# Use a base image with Python 3.10 or newer
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy rest of the app
COPY . .

# Run the Django app (adjust as needed)
CMD ["gunicorn", "dry.wsgi:application", "--bind", "0.0.0.0:8000"]
