#!/bin/bash
# Railway startup script

# Initialize database and seed data if not exists
if [ ! -f mgnrega.db ]; then
    echo "Initializing database..."
    python scripts/init_db.py
    echo "Seeding data..."
    python scripts/seed_data.py
fi

# Start the server
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
