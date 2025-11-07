# Use Python 3.11 base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (needed for psycopg2)
RUN apt-get update && apt-get install -y \
    build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of your Django project
COPY . .

# Expose port
EXPOSE 8000

# Run the Django development server
CMD ["python", "BankApp/manage.py", "runserver", "0.0.0.0:8000"]


