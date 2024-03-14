#!/bin/bash
# Prepare for django
python manage.py migrate
# Start uwsgi
uwsgi --ini uwsgi.ini
