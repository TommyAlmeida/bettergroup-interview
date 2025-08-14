#!/bin/bash
set -e

echo "Running Alembic migrations..."
alembic upgrade head

echo "Running fetch_and_populate script..."
python scripts/fetch_and_populate.py

echo "Starting Uvicorn..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000