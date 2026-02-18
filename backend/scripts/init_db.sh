#!/bin/bash
# Database Initialization Script
# Runs migrations and seeds exercise data

set -e  # Exit on error

echo "🔄 Waiting for PostgreSQL to be ready..."
sleep 3

echo "📦 Running Alembic migrations..."
cd /app
alembic upgrade head

echo "🌱 Seeding exercise library..."
python scripts/seed_exercises.py

echo "✅ Database initialized successfully!"
