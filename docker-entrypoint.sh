#!/bin/sh

set -e

until PGPASSWORD=secret psql -h db -U simulae -c '\q'; do
  >&2 echo "Postgres is unavailable - waiting..."
  sleep 1
done

if [ ! -f .env ]; then
    ln -s .env.example .env
    echo ".env file not found! Using .env.example"
fi

# Activate pipenv virtualenv
echo "Activating virtualenv"
source $(pipenv --venv)/bin/activate

# Apply database migrations
echo "Applying database migrations"
python manage.py migrate

# Load initial data
echo "Loading initial data"
python manage.py loaddata subjects topics questions users

# Test
echo "Testing"
python manage.py test

exec "$@"
