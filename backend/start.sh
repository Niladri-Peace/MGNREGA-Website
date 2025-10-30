#!/bin/bash
# Railway startup script
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
