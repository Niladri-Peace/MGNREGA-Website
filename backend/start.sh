#!/bin/bash
# Railway startup script

echo "=== MGNREGA Backend Startup ==="
echo "Checking for database..."

# Always initialize database (idempotent - creates tables if not exist)
echo "Running database initialization..."
python scripts/init_db.py

# Check if database has data
echo "Checking if database needs seeding..."
python scripts/seed_data.py

echo "Starting FastAPI server..."
# Start the server
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
