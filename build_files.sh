#!/bin/bash
set -e

echo "---- Python Version ----"
python --version
echo "---- Installing requirements ----"
pip install --upgrade pip
pip install -r requirements.txt

echo "---- Django setup ----"
mkdir -p static
python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate
