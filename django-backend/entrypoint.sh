#!/bin/sh

# Wait for Postgres
echo "Waiting for Postgres..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 0.1
done
echo "Postgres ready!"

# Run migrations
python3 manage.py migrate

# Start server
python3 manage.py runserver 0.0.0.0:8000

