import requests
import json
import requests
import json
import base64

schema_descriptions = {
    "customer_support": "This schema contains data related to customer support"
}

table_descriptions = {
    "conversations": "This table contains data related to customer conversations",
    "tickets": "This table contains data related to customer support tickets",
    "messages": "This table contains data related to customer messages",
    "ticket_history": "This table contains data related to ticket history",
}

column_descriptions = {
    "customer_support": {
        "conversations": {
            "conversation_id": "Unique identifier for the conversation",
        }
    }
}


def get_jwt_token():
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
        return jwt_token
    else:
        print(f"Failed to obtain token. Status code: {response.status_code}")


def update_schema_description(schema_id, description):
    jwt_token = get_jwt_token()
    url = f"http://localhost:8585/api/v1/databaseSchemas/{schema_id}"

    payload = json.dumps([
        {
            "op": "add",
            "path": "/description",
            "value": description
        }
    ])
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Authorization': f'Bearer {jwt_token}',
        'Content-Type': 'application/json-patch+json'
    }

    response = requests.request("PATCH", url, headers=headers, data=payload)

    print(response.text)


def update_table_description(table_id, description):
    jwt_token = get_jwt_token()
    url = f"http://localhost:8585/api/v1/tables/{table_id}"

    payload = json.dumps([
        {
            "op": "add",
            "path": "/description",
            "value": description
        }
    ])
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Authorization': f'Bearer {jwt_token}',
        'Content-Type': 'application/json-patch+json'
    }

    response = requests.request("PATCH", url, headers=headers, data=payload)

    print(response.text)


def get_schemas():
    # TODO - Add pagination
    jwt_token = get_jwt_token()
    url = "http://localhost:8585/api/v1/databaseSchemas"
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Authorization': f'Bearer {jwt_token}'
    }
    response = requests.request("GET", url, headers=headers).json()
    schema_data = response.get('data', [])
    schema_ids = {}
    for schema in schema_data:
        schema_id = schema.get('id')
        schema_name = schema.get('name')
        schema_ids[schema_name] = schema_id
    return schema_ids


def get_tables():
    jwt_token = get_jwt_token()
    url = "http://localhost:8585/api/v1/tables"
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Authorization': f'Bearer {jwt_token}'
    }

    tables_ids = {}
    while url:
        response = requests.request("GET", url, headers=headers).json()
        tables = response.get('data', [])
        for table in tables:
            table_id = table.get('id')
            table_name = table.get('name')
            tables_ids[table_name] = table_id
        paging = response.get('paging', {})
        url = f"http://localhost:8585/api/v1/tables?after={paging.get('after')}" if 'after' in paging else None
    return tables_ids


def get_table_columns(schema_name, table_name, db_name="postgres", db_service_name="sample_db"):
    jwt_token = get_jwt_token()
    url = f"http://localhost:8585/api/v1/tables/name/{db_service_name}.{db_name}.{schema_name}.{table_name}?fields=columns"

    payload = {}
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Authorization': f'Bearer {jwt_token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload).json()

    return response['columns']


def set_table_column_descriptions(table_id, column_definitions, column_descriptions):
    jwt_token = get_jwt_token()
    url = f"http://localhost:8585/api/v1/tables/{table_id}"

    payload = []
    for i, column in enumerate(column_definitions):
        column_name = column.get('name')
        if column_name in column_descriptions:
            description = column_descriptions[column_name]
            payload.append({
                "op": "add",
                "path": f"/columns/{i}/description",
                "value": description
            })

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Authorization': f'Bearer {jwt_token}',
        'Content-Type': 'application/json-patch+json'
    }

    response = requests.request("PATCH", url, headers=headers, data=json.dumps(payload))

    print(response.text)


# schemas = get_schemas()
# print(schemas)
# tables = get_tables()
# print(tables)
c = get_table_columns(schema_name="customer_support", table_name="conversations")
print(c)

# schema_id = "acfa42c1-d29e-46fc-b5da-9144e061647d"
# description = "This schema contains raw real estate data"
# update_schema_description(schema_id, description)
