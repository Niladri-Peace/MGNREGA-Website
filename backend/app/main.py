from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List, Optional
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import database and models
from .db.base import Base, engine, get_db, SessionLocal
from .db.models import State, District, MonthlyMetric

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize data on startup
logger.info("Checking database for initial data...")
db = SessionLocal()
try:
    state_count = db.query(State).count()
    if state_count == 0:
        logger.info("No data found. Running initial seed...")
        # Import and run seed function
        import sys
        from pathlib import Path
        scripts_path = Path(__file__).parent.parent / "scripts"
        sys.path.insert(0, str(scripts_path))
        from seed_data import main as seed_main
        seed_main()
        logger.info("Initial data seeded successfully!")
    else:
        logger.info(f"Database already has {state_count} states")
except Exception as e:
    logger.error(f"Error checking/seeding database: {e}")
finally:
    db.close()

# Initialize FastAPI app
app = FastAPI(
    title="MGNREGA District Performance Dashboard API",
    description="""
    Backend API for the MGNREGA District Performance Dashboard.
    Provides access to MGNREGA performance data for districts across India.
    """,
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (commented out - directories don't exist yet)
# app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates (commented out - directory doesn't exist yet)
# templates = Jinja2Templates(directory="templates")

# API Routes
@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": "1.0.0"}

@app.get("/api/v1/states", response_model=List[dict])
async def list_states(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """Get list of all states with their basic information"""
    try:
        states = db.query(State).offset(skip).limit(limit).all()
        return [
            {
                "id": state.id,
                "name": state.name,
                "code": state.code,
                "created_at": state.created_at.isoformat() if state.created_at else None,
                "updated_at": state.updated_at.isoformat() if state.updated_at else None
            }
            for state in states
        ]
    except Exception as e:
        logger.error(f"Error fetching states: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/v1/districts", response_model=List[dict])
async def list_districts(
    state_id: int,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 1000
):
    """Get list of districts for a specific state"""
    try:
        districts = db.query(District).filter(
            District.state_id == state_id
        ).offset(skip).limit(limit).all()
        
        return [
            {
                "id": district.id,
                "name": district.name,
                "code": district.code,
                "state_id": district.state_id,
                "centroid": {
                    "lat": district.centroid_lat,
                    "lon": district.centroid_lon
                } if district.centroid_lat and district.centroid_lon else None,
                "created_at": district.created_at.isoformat() if district.created_at else None,
                "updated_at": district.updated_at.isoformat() if district.updated_at else None
            }
            for district in districts
        ]
    except Exception as e:
        logger.error(f"Error fetching districts for state {state_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/v1/metrics/district/{district_id}", response_model=dict)
async def get_district_metrics(
    district_id: int,
    year: Optional[int] = None,
    month: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get MGNREGA metrics for a specific district"""
    try:
        query = db.query(MonthlyMetric).filter(
            MonthlyMetric.district_id == district_id
        )
        
        if year:
            query = query.filter(MonthlyMetric.year == year)
        if month:
            query = query.filter(MonthlyMetric.month == month)
        
        metrics = query.order_by(
            MonthlyMetric.year.desc(),
            MonthlyMetric.month.desc()
        ).first()
        
        if not metrics:
            raise HTTPException(
                status_code=404,
                detail=f"No metrics found for district {district_id}"
            )
        
        return {
            "district_id": metrics.district_id,
            "state_id": metrics.state_id,
            "year": metrics.year,
            "month": metrics.month,
            "households": {
                "total": metrics.total_households,
                "sc": metrics.sc_households,
                "st": metrics.st_households,
                "women": metrics.women_households
            },
            "works": {
                "total": metrics.total_works,
                "completed": metrics.completed_works,
                "in_progress": metrics.in_progress_works
            },
            "finances": {
                "total_funds": metrics.total_funds,
                "funds_utilized": metrics.funds_utilized,
                "wage_expenditure": metrics.wage_expenditure,
                "material_expenditure": metrics.material_expenditure
            },
            "person_days": {
                "total": metrics.total_person_days,
                "sc": metrics.sc_person_days,
                "st": metrics.st_person_days,
                "women": metrics.women_person_days
            },
            "metadata": {
                "is_latest": metrics.is_latest,
                "source_url": metrics.source_url,
                "updated_at": metrics.updated_at.isoformat() if metrics.updated_at else None
            }
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error fetching metrics for district {district_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/v1/metrics/district/{district_id}/history", response_model=List[dict])
async def get_district_metric_history(
    district_id: int,
    years: int = 2,  # Default to 2 years of history
    db: Session = Depends(get_db)
):
    """Get historical metrics for a district"""
    try:
        # Get the most recent month's data
        latest = db.query(MonthlyMetric).filter(
            MonthlyMetric.district_id == district_id
        ).order_by(
            MonthlyMetric.year.desc(),
            MonthlyMetric.month.desc()
        ).first()
        
        if not latest:
            raise HTTPException(
                status_code=404,
                detail=f"No metrics found for district {district_id}"
            )
        
        # Calculate date range
        from datetime import date
        from dateutil.relativedelta import relativedelta
        
        end_date = date(latest.year, latest.month, 1)
        start_date = end_date - relativedelta(years=years)
        
        # Get historical data
        history = db.query(MonthlyMetric).filter(
            MonthlyMetric.district_id == district_id,
            (
                (MonthlyMetric.year > start_date.year) |
                ((MonthlyMetric.year == start_date.year) & 
                 (MonthlyMetric.month >= start_date.month))
            )
        ).order_by(
            MonthlyMetric.year.asc(),
            MonthlyMetric.month.asc()
        ).all()
        
        return [
            {
                "year": m.year,
                "month": m.month,
                "households": m.total_households,
                "person_days": m.total_person_days,
                "works_completed": m.completed_works,
                "funds_utilized": m.funds_utilized
            }
            for m in history
        ]
        
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error fetching history for district {district_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/v1/districts/detect-by-location")
async def detect_district_by_location(
    lat: float,
    lon: float,
    db: Session = Depends(get_db)
):
    """Detect nearest district based on latitude and longitude"""
    try:
        from math import radians, cos, sin, asin, sqrt
        
        def haversine(lon1, lat1, lon2, lat2):
            """Calculate the great circle distance between two points on earth (in km)"""
            lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
            c = 2 * asin(sqrt(a))
            km = 6371 * c
            return km
        
        # Get all districts with coordinates
        districts = db.query(District, State).join(
            State, District.state_id == State.id
        ).filter(
            District.centroid_lat.isnot(None),
            District.centroid_lon.isnot(None)
        ).all()
        
        if not districts:
            raise HTTPException(status_code=404, detail="No districts with coordinates found")
        
        # Find nearest district
        nearest_district = None
        min_distance = float('inf')
        
        for district, state in districts:
            distance = haversine(lon, lat, district.centroid_lon, district.centroid_lat)
            if distance < min_distance:
                min_distance = distance
                nearest_district = (district, state)
        
        if not nearest_district:
            raise HTTPException(status_code=404, detail="Could not detect district")
        
        district, state = nearest_district
        
        # Calculate confidence based on distance (closer = higher confidence)
        # Within 50km = high confidence, beyond 200km = low confidence
        confidence = max(0, min(100, 100 - (min_distance / 2)))
        
        return {
            "id": district.id,
            "name": district.name,
            "state_name": state.name,
            "state_id": state.id,
            "distance_km": round(min_distance, 2),
            "confidence": round(confidence, 2)
        }
        
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error detecting district by location: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/v1/metrics/compare", response_model=List[dict])
async def compare_districts(
    district_ids: str,  # Comma-separated district IDs
    year: Optional[int] = None,
    month: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Compare metrics across multiple districts"""
    try:
        ids = [int(id.strip()) for id in district_ids.split(',')]
        
        query = db.query(MonthlyMetric, District).join(
            District, MonthlyMetric.district_id == District.id
        ).filter(MonthlyMetric.district_id.in_(ids))
        
        if year:
            query = query.filter(MonthlyMetric.year == year)
        if month:
            query = query.filter(MonthlyMetric.month == month)
        
        # Get latest for each district if no year/month specified
        if not year and not month:
            from sqlalchemy import func
            subq = db.query(
                MonthlyMetric.district_id,
                func.max(MonthlyMetric.year * 100 + MonthlyMetric.month).label('max_period')
            ).filter(
                MonthlyMetric.district_id.in_(ids)
            ).group_by(MonthlyMetric.district_id).subquery()
            
            query = db.query(MonthlyMetric, District).join(
                District, MonthlyMetric.district_id == District.id
            ).join(
                subq,
                (MonthlyMetric.district_id == subq.c.district_id) &
                ((MonthlyMetric.year * 100 + MonthlyMetric.month) == subq.c.max_period)
            )
        
        results = query.all()
        
        return [
            {
                "district_id": metric.district_id,
                "district_name": district.name,
                "year": metric.year,
                "month": metric.month,
                "total_households": metric.total_households,
                "total_person_days": metric.total_person_days,
                "completed_works": metric.completed_works,
                "funds_utilized": metric.funds_utilized,
                "wage_expenditure": metric.wage_expenditure
            }
            for metric, district in results
        ]
        
    except Exception as e:
        logger.error(f"Error comparing districts: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Error handlers
@app.exception_handler(404)
async def not_found_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc.detail) if hasattr(exc, 'detail') else "Resource not found"},
    )

@app.exception_handler(500)
async def server_error_exception_handler(request: Request, exc: Exception):
    logger.error(f"Server error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )

# For development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
