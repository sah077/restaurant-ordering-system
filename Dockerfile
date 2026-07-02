# ==============================================================
# Dockerfile for TastyBite Restaurant Ordering System
# Base image: official Python slim image (small size, fast builds)
# ==============================================================

FROM python:3.12-slim

# Prevent Python from writing .pyc files and buffering stdout/stderr
# (makes logs show up immediately in `docker logs`)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies needed by Pillow (image handling) and psycopg2 (if using Postgres later)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libjpeg-dev \
        zlib1g-dev \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first (this layer gets cached, so rebuilds are faster
# unless requirements.txt actually changes)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project code into the container
COPY . .

# Create directories for static/media files (in case they don't exist yet)
RUN mkdir -p /app/staticfiles /app/media

# Collect static files at build time so WhiteNoise can serve them
# (safe to run even if no static files change often)
RUN python manage.py collectstatic --no-input

# Expose the port Django/Gunicorn will run on
EXPOSE 1011

# Run database migrations, then start the Gunicorn production server
CMD ["sh", "-c", "python manage.py migrate && gunicorn restaurant_system.wsgi:application --bind 0.0.0.0:1011"]