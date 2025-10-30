"""
Initialize database tables
"""
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.base import Base, engine
from app.db.models import State, District, MonthlyMetric, APICache, DataSnapshot

def init_database():
    """Create all database tables"""
    print("=" * 60)
    print("Initializing Database Tables")
    print("=" * 60)
    
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✓ All tables created successfully!")
        
        # List created tables
        print("\nCreated tables:")
        for table in Base.metadata.sorted_tables:
            print(f"  - {table.name}")
            
    except Exception as e:
        print(f"✗ Error creating tables: {str(e)}")
        raise

if __name__ == "__main__":
    init_database()
