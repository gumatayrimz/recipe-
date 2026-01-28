#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Starting Build Process..."
pip install -r requirements.txt

echo "Collecting Static Files..."
python manage.py collectstatic --no-input

echo "Running Database Migrations..."
python manage.py migrate

echo "Build Process Complete!"
