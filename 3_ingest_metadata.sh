#!/bin/bash

set -e

echo -e "\n=== Setting up Python Virtual Environment ==="
python -m venv .openmetadata_venv
source .openmetadata_venv/bin/activate
pip install -r requirements.txt

cd src

echo -e "\n=== Running Metadata Ingestion ==="
python openmetadata/set_schema_metadata.py
python openmetadata/set_user_metadata.py

echo -e "\n=== Restoring Original Configuration ==="
mv openmetadata/database_connection.yaml.original openmetadata/database_connection.yaml
