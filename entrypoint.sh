#!/bin/bash

echo "Collecting static files"
python manage.py collectstatic --noinput

echo "Applying database migrations"
python manage.py migrate --noinput

#. /code/wait-for-it.sh "db:5432" -- uwsgi --ini "/code/config/uwsgi/uwsgi.ini"

echo "Invoking command from docker-compose file"
exec "$@"