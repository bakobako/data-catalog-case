import requests
import json
import base64
from typing import Dict, List, Optional
import yaml


class UserManager:
    def __init__(self, base_url: str, admin_email: str, admin_password: str):
        self.base_url = base_url.rstrip('/')
        self.admin_email = admin_email
        self.admin_password = admin_password
        self.jwt_token = None

    def _get_jwt_token(self) -> str:
        """Get JWT token for authentication"""
        if self.jwt_token:
            return self.jwt_token

        url = f"{self.base_url}/api/v1/users/login"
        headers = {"Content-Type": "application/json"}
        encoded_password = base64.b64encode(self.admin_password.encode()).decode()

        data = {
            "email": self.admin_email,
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
            'Content-Type': 'application/json'
        }

    def create_user(self, name: str, email: str, description: str,
                    display_name: Optional[str] = None, is_admin: bool = False) -> Dict:
        """Create a new user"""
        url = f"{self.base_url}/api/v1/users"

        # Generate a dummy password
        password = f"Password123!{name}"

        payload = {
            "name": name,
            "email": email,
            "description": description,
            "displayName": display_name or name,
            "isAdmin": is_admin,
            "isBot": False,
            "password": password,
            "confirmPassword": password,
            "createPasswordType": "ADMIN_CREATE"
        }

        response = requests.post(url, headers=self._get_headers(), json=payload)
        if response.status_code != 201:
            raise Exception(f"Failed to create user: {response.text}")

        return response.json()

    def list_users(self) -> List[Dict]:
        """List all non-bot users"""
        url = f"{self.base_url}/api/v1/users?limit=100&isBot=false"
        response = requests.get(url, headers=self._get_headers())

        if response.status_code != 200:
            raise Exception(f"Failed to list users: {response.text}")

        return response.json().get('data', [])

    def assign_schema_owner(self, schema_id: str, user_id: str) -> None:
        """Assign a user as the owner of a schema"""
        url = f"{self.base_url}/api/v1/databaseSchemas/{schema_id}"

        # Get user details first
        user_response = requests.get(
            f"{self.base_url}/api/v1/users/{user_id}",
            headers=self._get_headers()
        )
        if user_response.status_code != 200:
            raise Exception(f"Failed to get user details: {user_response.text}")

        user_data = user_response.json()

        payload = [
            {
                "op": "add",
                "path": "/owners/0",
                "value": {
                    "id": user_id,
                    "type": "user",
                    "name": user_data.get('name'),
                    "displayName": user_data.get('displayName'),
                    "description": user_data.get('description'),
                }
            }
        ]

        headers = self._get_headers()
        headers['Content-Type'] = 'application/json-patch+json'

        response = requests.patch(url, headers=headers, json=payload)
        if response.status_code != 200:
            raise Exception(f"Failed to assign schema owner: {response.text}")

    def setup_schema_owners_from_config(self, users_config_path: str) -> None:
        """Setup owners for schemas based on users configuration file"""
        print("Setting up schema owners from configuration...")

        # Load users configuration
        with open(users_config_path, 'r') as file:
            users_config = yaml.safe_load(file)

        # Get existing schemas
        url = f"{self.base_url}/api/v1/databaseSchemas"
        response = requests.get(url, headers=self._get_headers())
        if response.status_code != 200:
            raise Exception(f"Failed to get schemas: {response.text}")

        schemas = {
            schema['name']: schema['id']
            for schema in response.json().get('data', [])
        }

        # Process each user in the configuration
        for user_key, user_config in users_config.get('users', {}).items():
            try:
                # Create the user
                user = self.create_user(
                    name=user_config['name'],
                    email=user_config['email'],
                    description=user_config['description'],
                    display_name=user_config.get('display_name'),
                    is_admin=user_config.get('is_admin', False)
                )
                print(f"Created user {user_config['name']}")

                # Assign schemas to the user
                for schema_name in user_config.get('assigned_schemas', []):
                    if schema_name in schemas:
                        self.assign_schema_owner(schemas[schema_name], user['id'])
                        print(f"Assigned {user_config['name']} as owner of {schema_name}")
                    else:
                        print(f"Warning: Schema {schema_name} not found")

            except Exception as e:
                raise Exception(f"Error processing user {user_key}: {str(e)}")


if __name__ == "__main__":
    manager = UserManager(
        base_url="http://localhost:8585",
        admin_email="admin@open-metadata.org",
        admin_password="admin"
    )

    manager.setup_schema_owners_from_config("openmetadata/sample_metadata/user_metadata.yaml")