#!/bin/bash

echo "Creating migrations"
python manage.py makemigrations

echo "Migrating"
python manage.py migrate

echo "Loading Categories"
python manage.py loaddata categories.json

echo "Collecting static files"
python manage.py collectstatic --noinput

echo "Start server"
#python manage.py runserver 0.0.0.0:8000
python -m gunicorn library_manager.wsgi --bind 0.0.0.0:8000 --workers 8 --threads 2 --timeout 60
