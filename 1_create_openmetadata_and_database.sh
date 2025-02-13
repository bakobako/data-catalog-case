#!/bin/bash

set -e

echo "=== Starting Setup ==="

echo -e "\n=== Setting up Python Virtual Environment ==="
python -m venv .openmetadata_venv
source .openmetadata_venv/bin/activate
pip install -r requirements.txt

echo -e "\n=== Starting Docker of OpenMetadata and Postgres DB ==="
cd src/openmetadata
docker-compose -f docker-compose-postgres.yml up -d
cd ..

echo -e "\n=== Setting up Database Schema and Tables in Postgres ==="
python database_setup/database_setup.py "postgresql://user:pass@localhost:5433/postgres"

echo -e "\n=== Loading Sample Data to Postgres==="
python database_setup/load_sample_data.py "postgresql://user:pass@localhost:5433/postgres"

echo -e "\n=== Setup Complete! ==="
echo -e "\nOpenMetadata UI is available at: http://localhost:8585"
echo "Default credentials:"
echo "Username: admin@open-metadata.org"
echo "Password: admin"