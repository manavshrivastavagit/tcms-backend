#!/bin/bash

# Define the root directory of the project
PROJECT_NAME="myfastapiapp"
mkdir ${PROJECT_NAME}
cd ${PROJECT_NAME}

# Create main application folders and subfolders
mkdir -p app/{api/endpoints,models,schemas,services}
mkdir tests
mkdir alembic/versions

# Create initial Python packages and key files
echo "from fastapi import FastAPI" > app/main.py
echo "from sqlalchemy.ext.declarative import declarative_base" > app/models/base.py
echo "from pydantic import BaseModel" > app/schemas/__init__.py
echo "def get_db(): pass" > app/dependencies.py
echo "from fastapi import APIRouter" > app/api/api.py
touch app/__init__.py app/models/__init__.py app/services/__init__.py
touch app/api/__init__.py app/api/endpoints/__init__.py

# Create test files
echo "import pytest" > tests/test_main.py
touch tests/__init__.py tests/test_customer.py tests/test_plan.py

# Alembic configuration files
touch alembic/env.py
echo "from alembic import context" > alembic/script.py.mako

# Create root files
echo "FastAPI Application" > README.md
echo "python-dotenv==0.19.2" > requirements.txt
echo "*.pyc" > .gitignore
echo "DB_HOST=localhost" > .env

# Docker and docker-compose
echo "FROM python:3.9-slim" > Dockerfile
echo "version: '3.7'" > docker-compose.yml
echo "services:" >> docker-compose.yml
echo "  app:" >> docker-compose.yml
echo "    build: ." >> docker-compose.yml
echo "    ports:" >> docker-compose.yml
echo "      - '8000:8000'" >> docker-compose.yml

echo "Project directory structure setup completed."
