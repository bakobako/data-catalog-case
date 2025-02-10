import os
import pandas as pd
from database_definition.models.base import get_engine


def get_schema_and_table(filename: str):
    """Extract schema and table name from filename."""
    base = os.path.splitext(filename)[0]
    schema, table = base.split('___')
    return schema, table


def convert_datetime(value):
    """Convert a value to datetime, handling empty values and different formats."""
    if pd.isna(value) or value.strip() == '':
        return None
    try:
        return pd.to_datetime(value)
    except:
        return None


def load_sample_data(database_url: str, data_dir: str = 'sample_data'):
    """Load all CSV files into the database in specific order."""
    engine = get_engine(database_url)

    # Define loading order - start with tables that others depend on
    loading_order = [
        'sales___customers.csv',  # Load customers first
        'human_resources___departments.csv',
        'human_resources___employees.csv',
        'real_estate_listings___locations.csv',
        'real_estate_listings___raw_real_estate_listings.csv',
        'real_estate_listings___analysed_real_estate_listings.csv',
        'real_estate_listings___listing_photos.csv',
        'sales___transactions.csv',
        'sales___subscriptions.csv',
        'marketing___seo_targeting.csv',
        'marketing___seo_analytics.csv',
        'marketing___social_media_campaigns.csv',
        'marketing___social_media_ads.csv',
        'marketing___social_media_engagement.csv',
        'user_behaviour___email_tracking.csv',
        'user_behaviour___email_open_tracking.csv',
        'user_behaviour___website_visits.csv',
        'user_behaviour___page_views.csv',
        'user_behaviour___bounce_tracking.csv',
        'user_behaviour___email_click_tracking.csv',
        'customer_support___tickets.csv',
        'customer_support___conversations.csv',
        'customer_support___messages.csv',
        'customer_support___ticket_history.csv',
        'cloud_infrastructure___pipeline_runs.csv',
        'cloud_infrastructure___cloud_costs.csv'
    ]

    print(f"\nStarting data load in predefined order...")

    for csv_file in loading_order:
        schema, table = get_schema_and_table(csv_file)
        file_path = os.path.join(data_dir, csv_file)

        if not os.path.exists(file_path):
            print(f"Skipping {csv_file} (file not found)")
            continue

        try:
            print(f"\nLoading {csv_file} into {schema}.{table}...")
            df = pd.read_csv(file_path)

            # Convert timestamp columns to datetime
            for col in df.columns:
                if any(time_word in col.lower() for time_word in ['date', 'time', 'timestamp']):
                    df[col] = df[col].apply(convert_datetime)

            df.to_sql(
                table,
                engine,
                schema=schema,
                if_exists='append',
                index=False
            )
            print(f"Successfully loaded {len(df)} rows into {schema}.{table}")

        except Exception as e:
            print(f"Error loading {csv_file}: {str(e)}")
            raise

    print("\nAll sample data loaded successfully!")


def main():
    import sys
    if len(sys.argv) != 2:
        print("Usage: python load_sample_data.py <DATABASE_URL>")
        print("Example: python load_sample_data.py postgresql://user:pass@localhost:5432/dbname")
        sys.exit(1)

    database_url = sys.argv[1]
    load_sample_data(database_url)


if __name__ == "__main__":
    main()