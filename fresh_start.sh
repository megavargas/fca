#!/bin/bash
echo "Starting ..."

echo ">> Deleting old migrations"
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete

echo ">> Deleting database"
find . -name "db.sqlite3" -delete

echo ">> Running manage.py makemigrations"
python manage.py makemigrations

echo ">> Running manage.py migrate"
python manage.py migrate

echo "Creating super user"
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin@example.com', 'pass')" | python manage.py shell

echo "Populate database"
# python manage.py populate --development