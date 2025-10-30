"""
MGNREGA Data Service
Handles fetching data from data.gov.in API with caching and rate limiting
"""
import httpx
import logging
from typing import Optional, Dict, List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from tenacity import retry, stop_after_attempt, wait_exponential
import os

from ..db.models import State, District, MonthlyMetric, APICache

logger = logging.getLogger(__name__)

# Data.gov.in API configuration
DATA_GOV_API_KEY = os.getenv("DATA_GOV_API_KEY", "")
DATA_GOV_BASE_URL = "https://api.data.gov.in/resource"

# MGNREGA specific resource IDs (these would be actual IDs from data.gov.in)
MGNREGA_RESOURCE_ID = "9f8e8e3d-3b3a-4f3e-8e3d-3b3a4f3e8e3d"  # Example ID

class MGNREGAAPIService:
    """Service for interacting with MGNREGA data from data.gov.in"""
    
    def __init__(self, db: Session):
        self.db = db
        self.api_key = DATA_GOV_API_KEY
        self.base_url = DATA_GOV_BASE_URL
        
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def fetch_from_api(self, endpoint: str, params: Dict) -> Optional[Dict]:
        """
        Fetch data from data.gov.in API with retry logic
        """
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                params['api-key'] = self.api_key
                params['format'] = 'json'
                
                response = await client.get(
                    f"{self.base_url}/{endpoint}",
                    params=params
                )
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 429:
                    logger.warning("Rate limit hit, will retry...")
                    raise Exception("Rate limit exceeded")
                else:
                    logger.error(f"API error: {response.status_code}")
                    return None
                    
        except Exception as e:
            logger.error(f"Error fetching from API: {str(e)}")
            raise
    
    def get_cached_data(self, endpoint: str, parameters: Dict) -> Optional[Dict]:
        """
        Get cached API response if available and not expired
        """
        cache_entry = self.db.query(APICache).filter(
            APICache.endpoint == endpoint,
            APICache.parameters == parameters,
            APICache.expires_at > datetime.utcnow()
        ).first()
        
        if cache_entry:
            logger.info(f"Cache hit for {endpoint}")
            return cache_entry.response
        
        return None
    
    def cache_data(self, endpoint: str, parameters: Dict, response: Dict, ttl_hours: int = 24):
        """
        Cache API response with expiration
        """
        expires_at = datetime.utcnow() + timedelta(hours=ttl_hours)
        
        cache_entry = APICache(
            endpoint=endpoint,
            parameters=parameters,
            response=response,
            expires_at=expires_at
        )
        
        self.db.add(cache_entry)
        self.db.commit()
        logger.info(f"Cached data for {endpoint}")
    
    async def get_district_data(
        self, 
        state_code: str, 
        district_code: str,
        year: Optional[int] = None,
        month: Optional[int] = None
    ) -> Optional[Dict]:
        """
        Get MGNREGA data for a specific district
        Uses cache first, then falls back to API
        """
        # Prepare parameters
        params = {
            'state_code': state_code,
            'district_code': district_code,
        }
        
        if year:
            params['year'] = year
        if month:
            params['month'] = month
        
        # Check cache first
        cached = self.get_cached_data(MGNREGA_RESOURCE_ID, params)
        if cached:
            return cached
        
        # Fetch from API if not in cache
        try:
            data = await self.fetch_from_api(MGNREGA_RESOURCE_ID, params)
            if data:
                # Cache the response
                self.cache_data(MGNREGA_RESOURCE_ID, params, data)
                return data
        except Exception as e:
            logger.error(f"Failed to fetch from API: {str(e)}")
        
        # Return None if both cache and API fail
        return None
    
    async def sync_district_data(self, district_id: int):
        """
        Sync latest data for a district from the API to database
        """
        district = self.db.query(District).filter(District.id == district_id).first()
        if not district:
            logger.error(f"District {district_id} not found")
            return False
        
        state = self.db.query(State).filter(State.id == district.state_id).first()
        
        # Fetch data from API
        data = await self.get_district_data(
            state_code=state.code,
            district_code=district.code
        )
        
        if not data:
            logger.warning(f"No data available for district {district.name}")
            return False
        
        # Parse and store in database
        # This would parse the actual API response structure
        # For now, this is a placeholder
        try:
            # Extract metrics from API response
            # The actual structure depends on data.gov.in response format
            records = data.get('records', [])
            
            for record in records:
                # Create or update monthly metric
                # This is example code - adjust based on actual API response
                pass
            
            return True
            
        except Exception as e:
            logger.error(f"Error syncing data: {str(e)}")
            return False
    
    def get_fallback_data(self, district_id: int, year: int, month: int) -> Optional[Dict]:
        """
        Get data from local database as fallback when API is unavailable
        """
        metric = self.db.query(MonthlyMetric).filter(
            MonthlyMetric.district_id == district_id,
            MonthlyMetric.year == year,
            MonthlyMetric.month == month
        ).first()
        
        if metric:
            return {
                'total_households': metric.total_households,
                'sc_households': metric.sc_households,
                'st_households': metric.st_households,
                'women_households': metric.women_households,
                'total_works': metric.total_works,
                'completed_works': metric.completed_works,
                'in_progress_works': metric.in_progress_works,
                'total_funds': metric.total_funds,
                'funds_utilized': metric.funds_utilized,
                'wage_expenditure': metric.wage_expenditure,
                'material_expenditure': metric.material_expenditure,
                'total_person_days': metric.total_person_days,
                'sc_person_days': metric.sc_person_days,
                'st_person_days': metric.st_person_days,
                'women_person_days': metric.women_person_days,
            }
        
        return None
