#!/bin/bash
set -e

echo "Installing requirements..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Running Django setup..."
# mkdir -p static
python manage.py collectstatic --noinput
python manage.py migrate
