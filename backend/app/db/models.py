from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, JSON, BigInteger, Boolean, Text
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime

# Use JSON for SQLite compatibility (instead of JSONB)
JSONType = JSON

class State(Base):
    __tablename__ = "states"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    code = Column(String(2), unique=True, nullable=False)  # State code (e.g., 'UP', 'MH')
    created_at = Column(Date, default=datetime.utcnow)
    updated_at = Column(Date, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    districts = relationship("District", back_populates="state")
    metrics = relationship("MonthlyMetric", back_populates="state")

class District(Base):
    __tablename__ = "districts"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True, nullable=False)
    code = Column(String(10), index=True, nullable=True)  # District code from data.gov.in
    state_id = Column(Integer, ForeignKey("states.id"), nullable=False)
    centroid_lat = Column(Float, nullable=True)
    centroid_lon = Column(Float, nullable=True)
    boundary = Column(JSONType, nullable=True)  # GeoJSON boundary data
    created_at = Column(Date, default=datetime.utcnow)
    updated_at = Column(Date, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    state = relationship("State", back_populates="districts")
    metrics = relationship("MonthlyMetric", back_populates="district")

class MonthlyMetric(Base):
    __tablename__ = "monthly_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    district_id = Column(Integer, ForeignKey("districts.id"), nullable=False)
    state_id = Column(Integer, ForeignKey("states.id"), nullable=False)
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)  # 1-12
    
    # Beneficiary metrics
    total_households = Column(Integer, default=0)
    sc_households = Column(Integer, default=0)  # Scheduled Caste
    st_households = Column(Integer, default=0)  # Scheduled Tribe
    women_households = Column(Integer, default=0)
    
    # Work metrics
    total_works = Column(Integer, default=0)
    completed_works = Column(Integer, default=0)
    in_progress_works = Column(Integer, default=0)
    
    # Financial metrics
    total_funds = Column(Float, default=0.0)  # in INR
    funds_utilized = Column(Float, default=0.0)  # in INR
    wage_expenditure = Column(Float, default=0.0)  # in INR
    material_expenditure = Column(Float, default=0.0)  # in INR
    
    # Person days
    total_person_days = Column(Integer, default=0)
    sc_person_days = Column(Integer, default=0)
    st_person_days = Column(Integer, default=0)
    women_person_days = Column(Integer, default=0)
    
    # Metadata
    is_latest = Column(Boolean, default=False)
    source_url = Column(String(500), nullable=True)
    raw_data = Column(JSONType, nullable=True)  # Raw API response
    created_at = Column(Date, default=datetime.utcnow)
    updated_at = Column(Date, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    district = relationship("District", back_populates="metrics")
    state = relationship("State", back_populates="metrics")
    
    # Composite index for faster lookups
    # __table_args__ removed for SQLite compatibility

class APICache(Base):
    """For caching API responses to reduce load on data.gov.in"""
    __tablename__ = "api_cache"
    
    id = Column(Integer, primary_key=True, index=True)
    endpoint = Column(String(200), nullable=False, index=True)
    parameters = Column(JSONType, nullable=False)  # JSON-serialized request parameters
    response = Column(JSONType, nullable=False)    # JSON response
    created_at = Column(Date, default=datetime.utcnow)
    expires_at = Column(Date, nullable=False)   # When this cache entry should expire
    
    # Index for faster lookups
    # __table_args__ removed for SQLite compatibility

class DataSnapshot(Base):
    """For storing raw data snapshots from data.gov.in"""
    __tablename__ = "data_snapshots"
    
    id = Column(Integer, primary_key=True, index=True)
    snapshot_date = Column(Date, nullable=False, index=True)
    state_id = Column(Integer, ForeignKey("states.id"), nullable=True)
    district_id = Column(Integer, ForeignKey("districts.id"), nullable=True)
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    data_type = Column(String(50), nullable=False)  # e.g., 'monthly_metrics', 'district_list'
    s3_path = Column(String(500), nullable=True)   # Path to S3 if stored externally
    row_count = Column(Integer, default=0)
    status = Column(String(20), default='pending')  # pending, processing, completed, failed
    error_message = Column(String(500), nullable=True)
    created_at = Column(Date, default=datetime.utcnow)
    updated_at = Column(Date, default=datetime.utcnow, onupdate=datetime.utcnow)
