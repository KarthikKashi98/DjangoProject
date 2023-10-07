#!/bin/bash

# Create a virtual environment
echo "Creating a virtual environment..."

pip install psycopg2
pip install -r requirements.txt
python3 manage.py collectstatic --noinput
python3 manage.py makemigrations
python3 manage.py migrate


DJANGO_SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL}
DJANGO_SUPERUSER_USERNAME=${DJANGO_SUPERUSER_USERNAME}
DJANGO_SUPERUSER_PASSWORD=${DJANGO_SUPERUSER_PASSWORD}

python3.9 manage.py createsuperuser \
    --email $DJANGO_SUPERUSER_EMAIL \
    --username $DJANGO_SUPERUSER_USERNAME \
    --noinput || true
echo "your_password" | python manage.py shell -c "from django.contrib.auth.models import User; user=User.objects.get(username=$DJANGO_SUPERUSER_USERNAME); user.set_password($DJANGO_SUPERUSER_PASSWORD); user.save()"

