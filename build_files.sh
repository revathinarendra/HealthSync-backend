# #!/bin/bash

# # Ensure pip is available
# /usr/bin/python3.9 -m ensurepip --upgrade

# # Upgrade pip
# /usr/bin/python3.9 -m pip install --upgrade pip

# # Install dependencies from requirements.txt
# /usr/bin/python3.9 -m pip install -r requirements.txt

# # Create static directory if it doesn't exist
# mkdir -p /vercel/path0/static

# # Collect static files
# python3.9 manage.py collectstatic --noinput

# # Apply database migrations
# python3.9 manage.py makemigrations
# python3.9 manage.py migrate
#!/bin/bash

# Install virtualenv
python3.9 -m pip install --upgrade pip
python3.9 -m pip install virtualenv

# Create and activate virtual environment
python3.9 -m virtualenv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Apply database migrations
python manage.py makemigrations
python manage.py migrate
