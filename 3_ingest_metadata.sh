#!/bin/bash

set -e

echo -e "\n=== Setting up Python Virtual Environment ==="
python -m venv .openmetadata_venv
source .openmetadata_venv/bin/activate
pip install -r requirements.txt

cd src

echo -e "\n=== Running Metadata Ingestion - Schema, Table, and Column descriptions ==="
python openmetadata/set_schema_metadata.py

echo -e "\n=== Running Metadata Ingestion - User Metadata ==="
python openmetadata/set_user_metadata.py
