# Use an official Python runtime as a parent image
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire app directory into the container
COPY app/ /app/app

# Set PYTHONPATH to include the /app directory
ENV PYTHONPATH=/app

CMD ["tail", "-f", "/dev/null"]