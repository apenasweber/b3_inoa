#!/bin/bash
export PYTHONPATH="/app/b3_inoa:$PYTHONPATH"

# Wait for the DB to be ready
echo "Waiting for PostgreSQL to start..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

# Run migrations
python b3_inoa/manage.py makemigrations
python b3_inoa/manage.py migrate

# Create superuser if it does not exist
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser(os.environ.get('DJANGO_SUPERUSER_USERNAME'), os.environ.get('DJANGO_SUPERUSER_EMAIL'), os.environ.get('DJANGO_SUPERUSER_PASSWORD')) if not User.objects.filter(username=os.environ.get('DJANGO_SUPERUSER_USERNAME')).exists() else 0" | python b3_inoa/manage.py shell

# Start the Django development server
python b3_inoa/manage.py runserver 0.0.0.0:8000
echo "Django Server started on localhost/8000"
