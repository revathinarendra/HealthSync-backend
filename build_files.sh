#!/bin/bash

# Python setup
python -m ensurepip --upgrade
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# Django setup
python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate

