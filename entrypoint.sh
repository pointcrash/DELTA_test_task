#!/bin/sh -e

. .venv/bin/activate

cd fastapi-application

echo "Running Alembic migrations..."
alembic upgrade head

echo "Starting FastAPI..."
python run_main.py
