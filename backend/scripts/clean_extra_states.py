"""
Clean up extra states - keep only the 5 required states
"""
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.base import SessionLocal
from app.db.models import State, District, MonthlyMetric

def clean_extra_states():
    """Remove states that are not in the required 5"""
    db = SessionLocal()
    
    # States to KEEP
    keep_states = ["UP", "BR", "WB", "MH", "TN"]
    
    try:
        print("=" * 60)
        print("Cleaning Extra States")
        print("=" * 60)
        
        # Get all states
        all_states = db.query(State).all()
        print(f"\nFound {len(all_states)} states in database")
        
        # Find states to delete
        states_to_delete = [s for s in all_states if s.code not in keep_states]
        
        if not states_to_delete:
            print("\n✓ No extra states to delete. Database is clean!")
            return
        
        print(f"\nStates to delete: {len(states_to_delete)}")
        for state in states_to_delete:
            print(f"  - {state.name} ({state.code})")
        
        # Delete related data first
        for state in states_to_delete:
            # Delete monthly metrics
            metrics_deleted = db.query(MonthlyMetric).filter(
                MonthlyMetric.state_id == state.id
            ).delete()
            print(f"  Deleted {metrics_deleted} metrics for {state.name}")
            
            # Delete districts
            districts_deleted = db.query(District).filter(
                District.state_id == state.id
            ).delete()
            print(f"  Deleted {districts_deleted} districts for {state.name}")
            
            # Delete state
            db.delete(state)
            print(f"  Deleted state: {state.name}")
        
        db.commit()
        
        print("\n" + "=" * 60)
        print("✓ Cleanup completed successfully!")
        print("=" * 60)
        
        # Print summary
        remaining_states = db.query(State).all()
        print(f"\nRemaining states: {len(remaining_states)}")
        for state in remaining_states:
            district_count = db.query(District).filter(District.state_id == state.id).count()
            print(f"  - {state.name} ({state.code}): {district_count} districts")
        
    except Exception as e:
        print(f"\n✗ Error during cleanup: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    clean_extra_states()
