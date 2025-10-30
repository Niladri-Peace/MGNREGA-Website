"""
Seed script to populate the database with sample MGNREGA data
"""
import sys
import os
from datetime import datetime, timedelta
import random

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.base import SessionLocal
from app.db.models import State, District, MonthlyMetric

# Sample district data for multiple states
DISTRICTS_BY_STATE = {
    "UP": [
        {"name": "Lucknow", "code": "LKO", "lat": 26.8467, "lon": 80.9462},
        {"name": "Varanasi", "code": "VNS", "lat": 25.3176, "lon": 82.9739},
        {"name": "Agra", "code": "AGR", "lat": 27.1767, "lon": 78.0081},
        {"name": "Kanpur Nagar", "code": "KNP", "lat": 26.4499, "lon": 80.3319},
        {"name": "Prayagraj", "code": "PRG", "lat": 25.4358, "lon": 81.8463},
        {"name": "Gorakhpur", "code": "GKP", "lat": 26.7606, "lon": 83.3732},
        {"name": "Meerut", "code": "MRT", "lat": 28.9845, "lon": 77.7064},
        {"name": "Bareilly", "code": "BRE", "lat": 28.3670, "lon": 79.4304},
        {"name": "Aligarh", "code": "ALG", "lat": 27.8974, "lon": 78.0880},
        {"name": "Moradabad", "code": "MBD", "lat": 28.8389, "lon": 78.7378},
    ],
    "BR": [
        {"name": "Patna", "code": "PAT", "lat": 25.5941, "lon": 85.1376},
        {"name": "Gaya", "code": "GAY", "lat": 24.7955, "lon": 85.0002},
        {"name": "Muzaffarpur", "code": "MZF", "lat": 26.1225, "lon": 85.3906},
        {"name": "Bhagalpur", "code": "BGP", "lat": 25.2425, "lon": 86.9842},
        {"name": "Darbhanga", "code": "DBG", "lat": 26.1542, "lon": 85.8918},
        {"name": "Purnia", "code": "PUR", "lat": 25.7771, "lon": 87.4753},
        {"name": "Araria", "code": "ARA", "lat": 26.1497, "lon": 87.5156},
        {"name": "Saharsa", "code": "SAH", "lat": 25.8804, "lon": 86.5956},
    ],
    "WB": [
        {"name": "Kolkata", "code": "KOL", "lat": 22.5726, "lon": 88.3639},
        {"name": "North 24 Parganas", "code": "N24P", "lat": 22.6157, "lon": 88.4332},
        {"name": "South 24 Parganas", "code": "S24P", "lat": 22.1602, "lon": 88.4370},
        {"name": "Howrah", "code": "HWH", "lat": 22.5958, "lon": 88.2636},
        {"name": "Hooghly", "code": "HGL", "lat": 22.9089, "lon": 88.3967},
        {"name": "Nadia", "code": "NAD", "lat": 23.4710, "lon": 88.5565},
        {"name": "Murshidabad", "code": "MSD", "lat": 24.1833, "lon": 88.2833},
        {"name": "Darjeeling", "code": "DJL", "lat": 27.0410, "lon": 88.2663},
        {"name": "Jalpaiguri", "code": "JPG", "lat": 26.5167, "lon": 88.7167},
        {"name": "Malda", "code": "MLD", "lat": 25.0096, "lon": 88.1410},
    ],
    "MH": [
        {"name": "Mumbai", "code": "MUM", "lat": 19.0760, "lon": 72.8777},
        {"name": "Pune", "code": "PUN", "lat": 18.5204, "lon": 73.8567},
        {"name": "Nagpur", "code": "NAG", "lat": 21.1458, "lon": 79.0882},
        {"name": "Thane", "code": "THN", "lat": 19.2183, "lon": 72.9781},
        {"name": "Nashik", "code": "NSK", "lat": 19.9975, "lon": 73.7898},
        {"name": "Aurangabad", "code": "AUR", "lat": 19.8762, "lon": 75.3433},
        {"name": "Solapur", "code": "SLP", "lat": 17.6599, "lon": 75.9064},
        {"name": "Ahmednagar", "code": "AHM", "lat": 19.0948, "lon": 74.7480},
    ],
    "TN": [
        {"name": "Chennai", "code": "CHN", "lat": 13.0827, "lon": 80.2707},
        {"name": "Coimbatore", "code": "CBE", "lat": 11.0168, "lon": 76.9558},
        {"name": "Madurai", "code": "MDU", "lat": 9.9252, "lon": 78.1198},
        {"name": "Tiruchirappalli", "code": "TRY", "lat": 10.7905, "lon": 78.7047},
        {"name": "Salem", "code": "SLM", "lat": 11.6643, "lon": 78.1460},
        {"name": "Tirunelveli", "code": "TVL", "lat": 8.7139, "lon": 77.7567},
        {"name": "Erode", "code": "ERD", "lat": 11.3410, "lon": 77.7172},
        {"name": "Vellore", "code": "VLR", "lat": 12.9165, "lon": 79.1325},
    ],
}

def seed_states(db):
    """Seed states data - Only 5 major states"""
    states_data = [
        {"name": "Uttar Pradesh", "code": "UP"},
        {"name": "Bihar", "code": "BR"},
        {"name": "West Bengal", "code": "WB"},
        {"name": "Maharashtra", "code": "MH"},
        {"name": "Tamil Nadu", "code": "TN"},
    ]
    
    print("Seeding states...")
    for state_data in states_data:
        existing = db.query(State).filter(State.code == state_data["code"]).first()
        if not existing:
            state = State(**state_data)
            db.add(state)
            print(f"  Added: {state_data['name']}")
        else:
            print(f"  Exists: {state_data['name']}")
    
    db.commit()
    print(f"✓ States seeded: {len(states_data)}")

def seed_districts(db):
    """Seed districts data for multiple states"""
    print("\nSeeding districts for all states...")
    
    total_districts = 0
    for state_code, districts_list in DISTRICTS_BY_STATE.items():
        state = db.query(State).filter(State.code == state_code).first()
        if not state:
            print(f"  Warning: State {state_code} not found, skipping...")
            continue
        
        print(f"\n  Seeding {state.name} ({state_code})...")
        for district_data in districts_list:
            existing = db.query(District).filter(
                District.name == district_data["name"],
                District.state_id == state.id
            ).first()
            
            if not existing:
                district = District(
                    name=district_data["name"],
                    code=district_data["code"],
                    state_id=state.id,
                    centroid_lat=district_data["lat"],
                    centroid_lon=district_data["lon"]
                )
                db.add(district)
                print(f"    Added: {district_data['name']}")
                total_districts += 1
            else:
                print(f"    Exists: {district_data['name']}")
    
    db.commit()
    print(f"\n✓ Districts seeded: {total_districts} new districts")

def generate_monthly_metrics(district_id, state_id, year, month):
    """Generate realistic sample metrics"""
    base_households = random.randint(5000, 15000)
    base_person_days = base_households * random.randint(20, 40)
    base_funds = base_person_days * random.randint(250, 350)
    
    return {
        "district_id": district_id,
        "state_id": state_id,
        "year": year,
        "month": month,
        "total_households": base_households,
        "sc_households": int(base_households * random.uniform(0.15, 0.25)),
        "st_households": int(base_households * random.uniform(0.05, 0.15)),
        "women_households": int(base_households * random.uniform(0.40, 0.55)),
        "total_works": random.randint(30, 80),
        "completed_works": random.randint(15, 40),
        "in_progress_works": random.randint(10, 30),
        "total_funds": base_funds,
        "funds_utilized": base_funds * random.uniform(0.70, 0.95),
        "wage_expenditure": base_funds * random.uniform(0.55, 0.70),
        "material_expenditure": base_funds * random.uniform(0.15, 0.30),
        "total_person_days": base_person_days,
        "sc_person_days": int(base_person_days * random.uniform(0.15, 0.25)),
        "st_person_days": int(base_person_days * random.uniform(0.05, 0.15)),
        "women_person_days": int(base_person_days * random.uniform(0.40, 0.55)),
        "is_latest": False,
        "source_url": "https://data.gov.in/mgnrega"
    }

def seed_monthly_metrics(db):
    """Seed monthly metrics for all districts"""
    districts = db.query(District).all()
    
    print(f"\nSeeding monthly metrics for {len(districts)} districts...")
    
    # Generate data for last 12 months
    current_date = datetime.now()
    months_to_generate = 12
    
    total_added = 0
    for district in districts:
        for i in range(months_to_generate):
            date = current_date - timedelta(days=30 * i)
            year = date.year
            month = date.month
            
            # Check if already exists
            existing = db.query(MonthlyMetric).filter(
                MonthlyMetric.district_id == district.id,
                MonthlyMetric.year == year,
                MonthlyMetric.month == month
            ).first()
            
            if not existing:
                metrics = generate_monthly_metrics(
                    district.id,
                    district.state_id,
                    year,
                    month
                )
                # Mark most recent as latest
                if i == 0:
                    metrics["is_latest"] = True
                
                metric = MonthlyMetric(**metrics)
                db.add(metric)
                total_added += 1
        
        print(f"  Added metrics for: {district.name}")
    
    db.commit()
    print(f"✓ Monthly metrics seeded: {total_added} records")

def main():
    """Main seeding function"""
    print("=" * 60)
    print("MGNREGA Dashboard - Database Seeding")
    print("=" * 60)
    
    db = SessionLocal()
    try:
        seed_states(db)
        seed_districts(db)
        seed_monthly_metrics(db)
        
        print("\n" + "=" * 60)
        print("✓ Database seeding completed successfully!")
        print("=" * 60)
        
        # Print summary
        states_count = db.query(State).count()
        districts_count = db.query(District).count()
        metrics_count = db.query(MonthlyMetric).count()
        
        print(f"\nDatabase Summary:")
        print(f"  States: {states_count}")
        print(f"  Districts: {districts_count}")
        print(f"  Monthly Metrics: {metrics_count}")
        
    except Exception as e:
        print(f"\n✗ Error during seeding: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()
