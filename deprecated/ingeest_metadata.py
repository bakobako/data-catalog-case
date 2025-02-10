import os
from metadata.ingestion.ometa.ometa_api import OpenMetadata
from metadata.generated.schema.entity.services.connections.database.postgresConnection import PostgresConnection
from metadata.generated.schema.entity.services.databaseService import DatabaseService
from metadata.generated.schema.api.services.createDatabaseService import CreateDatabaseServiceRequest
from metadata.generated.schema.security.client.openMetadataJWTClientConfig import OpenMetadataJWTClientConfig


import requests
import json
import base64

url = "http://localhost:8585/api/v1/users/login"
headers = {"Content-Type": "application/json"}
password = "admin"
encoded_password = base64.b64encode(password.encode()).decode()  # Correctly encode and decode

data = {
    "email": "admin@open-metadata.org",
    "password": encoded_password  # Ensure this is a proper string
}

response = requests.post(url, headers=headers, data=json.dumps(data))
if response.status_code == 200:
    jwt_token = response.json().get("accessToken")
else:
    print(f"Failed to obtain token. Status code: {response.status_code}")

print(jwt_token)

#
# # OpenMetadata server configuration
# server_config = OpenMetadataJWTClientConfig(
#     jwtToken=jwt_token
# )
#
#
# # Initialize OpenMetadata client
# metadata = OpenMetadata(server_config)
#
# # PostgreSQL connection details
# postgres_connection = PostgresConnection(
#     username="bako",
#     password="vahmoh-vavQi2-nenxeq",
#     hostPort="db-bytovy-lovec.c962a8y428jz.eu-north-1.rds.amazonaws.com:5432",
#     database="sample"
# )
#
# # Create database service
# database_service = CreateDatabaseServiceRequest(
#     name="postgres_service",
#     serviceType="Postgres",
#     connection=postgres_connection
# )
#
# # Create the service in OpenMetadata
# created_service = metadata.create_or_update(database_service)
#
# # List tables in the database
# tables = metadata.list_entities(entity=DatabaseService, service_name="postgres_service")
#
# # Print the table names
# print("Tables in the database:")
# for table in tables:
#     print(table.name)
#
# # Close the connection
# metadata.close()
