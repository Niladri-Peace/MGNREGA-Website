import os
import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from sqlalchemy.orm import Session
import pandas as pd

from ..db.models import State, District, MonthlyMetric, DataSnapshot, APICache
from ..db.base import get_db

# Configure logging
logger = logging.getLogger(__name__)

class DataGovClient:
    """Client for interacting with data.gov.in API"""
    
    BASE_URL = "https://api.data.gov.in/resource"
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("DATA_GOV_API_KEY")
        if not self.api_key:
            raise ValueError("DATA_GOV_API_KEY environment variable not set")
        
        self.client = httpx.AsyncClient(timeout=30.0)
        
    async def close(self):
        await self.client.aclose()
        
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((httpx.RequestError, httpx.HTTPStatusError))
    )
    async def _make_request(self, endpoint: str, params: Dict[str, Any]) -> Dict:
        """Make a request to the data.gov.in API with retries"""
        url = f"{self.BASE_URL}/{endpoint}"
        params = {"api-key": self.api_key, "format": "json", **params}
        
        try:
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error {e.response.status_code} for {endpoint}: {e}")
            if e.response.status_code == 429:  # Rate limited
                retry_after = int(e.response.headers.get("Retry-After", 60))
                logger.warning(f"Rate limited. Retrying after {retry_after} seconds.")
                await asyncio.sleep(retry_after)
            raise
        except Exception as e:
            logger.error(f"Error making request to {endpoint}: {e}")
            raise

class DataIngestionService:
    """Service for ingesting MGNREGA data from data.gov.in"""
    
    def __init__(self, db: Session):
        self.db = db
        self.client = DataGovClient()
        
    async def sync_all_data(self):
        """Synchronize all available MGNREGA data"""
        logger.info("Starting full MGNREGA data synchronization")
        
        try:
            # Step 1: Sync states
            await self.sync_states()
            
            # Step 2: Sync districts for each state
            states = self.db.query(State).all()
            for state in states:
                await self.sync_districts(state.id)
            
            # Step 3: Sync metrics for each district
            districts = self.db.query(District).all()
            for district in districts:
                await self.sync_district_metrics(district.id)
                
            logger.info("MGNREGA data synchronization completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error during data synchronization: {e}", exc_info=True)
            return False
    
    async def sync_states(self) -> List[State]:
        """Synchronize states data"""
        logger.info("Synchronizing states...")
        
        # This is a mock implementation - replace with actual API call
        # Example: data = await self.client._make_request("mgnrega_states", {})
        
        # Mock data - replace with actual API response
        states_data = [
            {"state_name": "Uttar Pradesh", "state_code": "UP"},
            {"state_name": "Bihar", "state_code": "BR"},
            # Add more states as needed
        ]
        
        states = []
        for state_data in states_data:
            state = self.db.query(State).filter(
                State.code == state_data["state_code"]
            ).first()
            
            if not state:
                state = State(
                    name=state_data["state_name"],
                    code=state_data["state_code"]
                )
                self.db.add(state)
                self.db.commit()
                self.db.refresh(state)
                logger.info(f"Added new state: {state.name} ({state.code})")
            else:
                logger.debug(f"State already exists: {state.name} ({state.code})")
                
            states.append(state)
            
        return states
    
    async def sync_districts(self, state_id: int) -> List[District]:
        """Synchronize districts for a state"""
        state = self.db.query(State).get(state_id)
        if not state:
            raise ValueError(f"State with ID {state_id} not found")
            
        logger.info(f"Synchronizing districts for {state.name}...")
        
        # This is a mock implementation - replace with actual API call
        # Example: data = await self.client._make_request("mgnrega_districts", {"filters[state_code]": state.code})
        
        # Mock data - replace with actual API response
        districts_data = [
            {"district_name": "Lucknow", "district_code": "LKO"},
            {"district_name": "Varanasi", "district_code": "VNS"},
            # Add more districts as needed
        ]
        
        districts = []
        for district_data in districts_data:
            district = self.db.query(District).filter(
                District.state_id == state_id,
                District.name == district_data["district_name"]
            ).first()
            
            if not district:
                district = District(
                    name=district_data["district_name"],
                    code=district_data.get("district_code"),
                    state_id=state_id
                )
                self.db.add(district)
                self.db.commit()
                self.db.refresh(district)
                logger.info(f"Added new district: {district.name}, {state.code}")
            else:
                logger.debug(f"District already exists: {district.name}, {state.code}")
                
            districts.append(district)
            
        return districts
    
    async def sync_district_metrics(self, district_id: int) -> List[MonthlyMetric]:
        """Synchronize metrics for a district"""
        district = self.db.query(District).get(district_id)
        if not district:
            raise ValueError(f"District with ID {district_id} not found")
            
        logger.info(f"Synchronizing metrics for {district.name}, {district.state.code}...")
        
        # This is a mock implementation - replace with actual API call
        # Example: data = await self.client._make_request("mgnrega_metrics", {
        #     "filters[state_code]": district.state.code,
        #     "filters[district_code]": district.code
        # })
        
        # Mock data - replace with actual API response
        current_year = datetime.now().year
        metrics_data = [
            {
                "year": current_year - 1,
                "month": 12,
                "total_households": 5000,
                "sc_households": 1000,
                "st_households": 800,
                "women_households": 2000,
                "total_works": 50,
                "completed_works": 30,
                "in_progress_works": 20,
                "total_funds": 5000000,
                "funds_utilized": 4500000,
                "wage_expenditure": 3000000,
                "material_expenditure": 1500000,
                "total_person_days": 25000,
                "sc_person_days": 5000,
                "st_person_days": 4000,
                "women_person_days": 12000,
                "is_latest": False
            },
            # Add more months as needed
        ]
        
        metrics = []
        for metric_data in metrics_data:
            # Check if we already have this data
            existing = self.db.query(MonthlyMetric).filter(
                MonthlyMetric.district_id == district_id,
                MonthlyMetric.year == metric_data["year"],
                MonthlyMetric.month == metric_data["month"]
            ).first()
            
            if existing:
                logger.debug(f"Metrics already exist for {district.name}, {metric_data['year']}-{metric_data['month']}")
                metrics.append(existing)
                continue
                
            # Create new metric
            metric = MonthlyMetric(
                district_id=district_id,
                state_id=district.state_id,
                year=metric_data["year"],
                month=metric_data["month"],
                total_households=metric_data["total_households"],
                sc_households=metric_data["sc_households"],
                st_households=metric_data["st_households"],
                women_households=metric_data["women_households"],
                total_works=metric_data["total_works"],
                completed_works=metric_data["completed_works"],
                in_progress_works=metric_data["in_progress_works"],
                total_funds=metric_data["total_funds"],
                funds_utilized=metric_data["funds_utilized"],
                wage_expenditure=metric_data["wage_expenditure"],
                material_expenditure=metric_data["material_expenditure"],
                total_person_days=metric_data["total_person_days"],
                sc_person_days=metric_data["sc_person_days"],
                st_person_days=metric_data["st_person_days"],
                women_person_days=metric_data["women_person_days"],
                is_latest=metric_data.get("is_latest", False),
                source_url="https://data.gov.in/..."  # Replace with actual source URL
            )
            
            self.db.add(metric)
            self.db.commit()
            self.db.refresh(metric)
            
            logger.info(f"Added metrics for {district.name}, {metric.year}-{metric.month}")
            metrics.append(metric)
            
        return metrics
    
    async def create_snapshot(self, data_type: str, state_id: int = None, district_id: int = None) -> DataSnapshot:
        """Create a snapshot of the current data"""
        snapshot = DataSnapshot(
            snapshot_date=datetime.utcnow(),
            state_id=state_id,
            district_id=district_id,
            data_type=data_type,
            status="completed",
            row_count=0  # Will be updated
        )
        
        self.db.add(snapshot)
        self.db.commit()
        self.db.refresh(snapshot)
        
        return snapshot

# For testing
def test_sync():
    db = next(get_db())
    try:
        import asyncio
        service = DataIngestionService(db)
        asyncio.run(service.sync_all_data())
    finally:
        db.close()

if __name__ == "__main__":
    test_sync()
