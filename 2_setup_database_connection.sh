#!/bin/bash

set -e

echo -e "\n=== Setting up Python Virtual Environment ==="
python -m venv .openmetadata_venv
source .openmetadata_venv/bin/activate
pip install -r requirements.txt

echo -e "\n=== Setting Database Connection In OpenMetadata ==="
ENCODED_PASSWORD=$(echo -n "admin" | base64)
JWT_TOKEN=$(curl -X POST http://localhost:8585/api/v1/users/login \
  -H 'Content-Type: application/json' \
  -d "{\"email\":\"admin@open-metadata.org\", \"password\":\"$ENCODED_PASSWORD\"}" \
  | jq -r '.accessToken')
cp openmetadata/database_connection.yaml openmetadata/database_connection.yaml.original
sed "s/{jwt_token}/$JWT_TOKEN/" openmetadata/database_connection.yaml.original > openmetadata/database_connection.yaml
python -m metadata ingest -c openmetadata/database_connection.yaml

echo -e "\n=== Restoring Original Configuration ==="
mv openmetadata/database_connection.yaml.original openmetadata/database_connection.yaml
