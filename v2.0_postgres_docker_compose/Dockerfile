# --------------------
# Dockerfile for Python ETL Pipeline
# Author:             Dániel Varga
# Created:            2025-08-15
# Last Modified:      2025-08-15
#
# Description:
# This Dockerfile builds a Python environment for an ETL pipeline that interacts with Postgres.
# - Base image: Python 3
# - Sets working directory to /app
# - Installs Python dependencies from requirements.txt
# - Installs PostgreSQL client tools (pg_isready) to allow the container to wait for Postgres readiness
# - Copies the full project into the container
# - Default command runs the main ETL script (main.py)
# --------------------

    
FROM python:3

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

COPY . .

CMD ["python", "main.py"]

