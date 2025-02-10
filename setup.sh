#!/bin/bash

set -e  # Exit on any error

echo "=== Starting Setup ==="

# Step 1: Create and activate virtual environment
echo -e "\n=== Setting up Python Virtual Environment ==="
python -m venv .openmetadata_venv
source .openmetadata_venv/bin/activate
pip install -r full_requirements.txt

# Step 2: Start Docker Compose
echo -e "\n=== Starting Docker Compose Services ==="
cd openmetadata-docker
docker-compose -f docker-compose-postgres.yml up -d
cd ..

## Step 3: Setup Database Schema and Tables
#echo -e "\n=== Setting up Database Schema and Tables ==="
#python database_definition/database_definition.py
#
## Step 4: Load Sample Data
#echo -e "\n=== Loading Sample Data ==="
#python load_sample_data.py "postgresql://user:pass@localhost:5433/postgres"

# Step 5: Get JWT token and update connection YAML
echo -e "\n=== Getting JWT Token ==="
ENCODED_PASSWORD=$(echo -n "admin" | base64)
JWT_TOKEN=$(curl -X POST http://localhost:8585/api/v1/users/login \
  -H 'Content-Type: application/json' \
  -d "{\"email\":\"admin@open-metadata.org\", \"password\":\"$ENCODED_PASSWORD\"}" \
  | jq -r '.accessToken')

echo -e "\n=== Updating Database Connection YAML ==="
cp openmetadata-docker/database_connection.yaml openmetadata-docker/database_connection.yaml.original
sed "s/{jwt_token}/$JWT_TOKEN/" openmetadata-docker/database_connection.yaml.original > openmetadata-docker/database_connection.yaml
python -m metadata ingest -c openmetadata-docker/database_connection.yaml


# Step 6: Run Metadata Ingestion
echo -e "\n=== Running Metadata Ingestion ==="
python metadata_update.py

# Step 7: Restore original connection YAML
echo -e "\n=== Restoring Original Configuration ==="
mv openmetadata-docker/database_connection.yaml.original openmetadata-docker/database_connection.yaml


# Step 7: Cleanup - deactivate and remove virtual environment
echo -e "\n=== Cleaning up ==="
deactivate
rm -rf .openmetadata_venv

echo -e "\n=== Setup Complete! ==="
echo -e "\nOpenMetadata UI is available at: http://localhost:8585"
echo "Default credentials:"
echo "Username: admin@open-metadata.org"
echo "Password: admin"