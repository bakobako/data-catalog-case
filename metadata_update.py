import requests
import json
import base64
import yaml
from typing import Dict, List, Optional


class MetadataUpdater:
    def __init__(self, base_url: str, email: str, password: str):
        self.base_url = base_url.rstrip('/')
        self.email = email
        self.password = password
        self.jwt_token = None

    def _get_jwt_token(self) -> str:
        """Get JWT token for authentication"""
        if self.jwt_token:
            return self.jwt_token

        url = f"{self.base_url}/api/v1/users/login"
        headers = {"Content-Type": "application/json"}
        encoded_password = base64.b64encode(self.password.encode()).decode()

        data = {
            "email": self.email,
            "password": encoded_password
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            self.jwt_token = response.json().get("accessToken")
            return self.jwt_token
        else:
            raise Exception(f"Failed to obtain token. Status code: {response.status_code}")

    def _get_headers(self) -> Dict:
        """Get headers with JWT token"""
        return {
            'Accept': 'application/json, text/plain, */*',
            'Authorization': f'Bearer {self._get_jwt_token()}',
            'Content-Type': 'application/json-patch+json'
        }

    def update_schema_description(self, schema_id: str, description: str) -> None:
        """Update schema description"""
        url = f"{self.base_url}/api/v1/databaseSchemas/{schema_id}"
        payload = json.dumps([
            {
                "op": "add",
                "path": "/description",
                "value": description
            }
        ])
        response = requests.patch(url, headers=self._get_headers(), data=payload)
        if response.status_code != 200:
            raise Exception(f"Failed to update schema description: {response.text}")

    def update_table_description(self, table_id: str, description: str) -> None:
        """Update table description"""
        url = f"{self.base_url}/api/v1/tables/{table_id}"
        payload = json.dumps([
            {
                "op": "add",
                "path": "/description",
                "value": description
            }
        ])
        response = requests.patch(url, headers=self._get_headers(), data=payload)
        if response.status_code != 200:
            raise Exception(f"Failed to update table description: {response.text}")

    def get_schemas(self) -> Dict[str, str]:
        """Get all schemas and their IDs"""
        url = f"{self.base_url}/api/v1/databaseSchemas"
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Authorization': f'Bearer {self._get_jwt_token()}'
        }
        response = requests.get(url, headers=headers).json()
        return {
            schema.get('name'): schema.get('id')
            for schema in response.get('data', [])
        }

    def get_tables(self) -> Dict[str, str]:
        """Get all tables and their IDs"""
        url = f"{self.base_url}/api/v1/tables"
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Authorization': f'Bearer {self._get_jwt_token()}'
        }

        tables_ids = {}
        while url:
            response = requests.get(url, headers=headers).json()
            tables = response.get('data', [])
            for table in tables:
                tables_ids[table.get('name')] = table.get('id')
            paging = response.get('paging', {})
            url = f"{self.base_url}/api/v1/tables?after={paging.get('after')}" if 'after' in paging else None
        return tables_ids

    def get_table_columns(self, schema_name: str, table_name: str, db_name: str = "postgres",
                          db_service_name: str = "sample_db") -> List[Dict]:
        """Get columns for a specific table"""
        url = f"{self.base_url}/api/v1/tables/name/{db_service_name}.{db_name}.{schema_name}.{table_name}?fields=columns"
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Authorization': f'Bearer {self._get_jwt_token()}'
        }
        response = requests.get(url, headers=headers).json()
        return response['columns']

    def set_table_column_descriptions(self, table_id: str, column_definitions: List[Dict],
                                      column_descriptions: Dict[str, str]) -> None:
        """Update column descriptions for a table"""
        url = f"{self.base_url}/api/v1/tables/{table_id}"
        payload = []

        for i, column in enumerate(column_definitions):
            column_name = column.get('name')
            if column_name in column_descriptions:
                payload.append({
                    "op": "add",
                    "path": f"/columns/{i}/description",
                    "value": column_descriptions[column_name]
                })

        if payload:
            response = requests.patch(url, headers=self._get_headers(), data=json.dumps(payload))
            if response.status_code != 200:
                raise Exception(f"Failed to update column descriptions: {response.text}")

    def update_metadata_from_yaml(self, yaml_file_path: str) -> None:
        """Update metadata using a YAML configuration file"""
        print(f"Updating metadata from {yaml_file_path}")
        with open(yaml_file_path, 'r') as file:
            metadata = yaml.safe_load(file)

        schemas = self.get_schemas()
        tables = self.get_tables()

        # Update schema descriptions
        for schema_name, schema_data in metadata.get('schemas', {}).items():
            if schema_name in schemas:
                print(f"Updating schema description for {schema_name}")
                self.update_schema_description(schemas[schema_name], schema_data['description'])

        # Update table and column descriptions
        for schema_name, schema_data in metadata.get('schemas', {}).items():
            for table_name, table_data in schema_data.get('tables', {}).items():
                if table_name in tables:
                    # Update table description
                    self.update_table_description(tables[table_name], table_data['description'])

                    # Update column descriptions
                    if 'columns' in table_data:
                        column_definitions = self.get_table_columns(schema_name, table_name)
                        self.set_table_column_descriptions(
                            tables[table_name],
                            column_definitions,
                            table_data['columns']
                        )


updater = MetadataUpdater(
    base_url="http://localhost:8585",
    email="admin@open-metadata.org",
    password="admin"
)

# Update metadata from YAML file
updater.update_metadata_from_yaml("metadata.yaml")
