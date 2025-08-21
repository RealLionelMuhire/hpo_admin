#!/usr/bin/env bash
# Build script for Render

set -o errexit  # exit on error

# Install dependencies
pip install -r requirements.txt

# Collect static files
python3 manage.py collectstatic --no-input

# Run migrations
python3 manage.py migrate

# Create superuser if none exists
python3 manage.py create_superuser_if_none_exists
