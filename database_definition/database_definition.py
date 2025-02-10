import os
import sys
from sqlalchemy import create_engine, text
from models.base import Base, get_engine
from models.sales.models import *
from models.real_estate_listings.models import *
from models.real_estate_trackers.models import *
from models.cloud_infrastructure.models import *
from models.human_resources.models import *
from models.customer_support.models import *
from models.user_behaviour.models import *
from models.marketing.models import *
from models.location_amenities.models import *
from models.czech_market_data.models import *


def create_schemas(engine):
    schemas = [obj for obj in os.listdir('database_definition/models') if not obj.endswith('.py')]
    with engine.connect() as connection:
        for schema in schemas:
            connection.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema}"))
            print(f"Schema '{schema}' created (if it didn't already exist).")


# Function to create all tables
def create_tables(engine):
    Base.metadata.create_all(bind=engine)
    print("All tables have been created successfully!")


def execute_sql_from_file(connection, file_path):
    with open(file_path, 'r') as file:
        sql = file.read()
        connection.execute(text(sql))


# Main function
def main(database_url):
    engine = get_engine(database_url)
    create_schemas(engine)
    create_tables(engine)


if __name__ == "__main__":
    main("postgresql://user:pass@localhost:5433/postgres")
