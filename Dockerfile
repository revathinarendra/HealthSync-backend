FROM python:3.10-bookworm


# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies and security patches
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose and run
CMD ["gunicorn", "dry.wsgi:application", "--bind", "0.0.0.0:8000"]
