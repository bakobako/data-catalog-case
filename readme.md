# Real Estate Data Catalog Case Study

## Overview
This project implements a data catalog system for a real estate data warehouse using OpenMetadata. 
The system allows users to explore both technical and business information about available schemas, tables, and columns.
The sample data represents a fictitious real estate company that provides property listings and 
valuation services for buyers. The data model encompasses various aspects of the business including property 
listings, market analysis, customer interactions, and operational data.

## Task given

Design a data cataloging system for a data warehouse so that a user can explore technical and business 
information about available schemas, tables and columns.

* Automatically ingest free public datasets (from Kaggle or elsewhere) to a database system of your choice. Include at least 10 schemas, each should have multiple tables.
* Create a data model representing the descriptions of your data. Include business information (e.g. what is the context of a column) which can be originating from a static extract.
* Present this metadata information to a user.
* Optionally, come up with an automated way to gather business information from users to enrich technical metadata without description.
* Store your source codes in a Git repository.

## Project Structure
- `src/database_setup/`: Database schema definitions and sample data loading scripts
- `src/openmetadata/`: OpenMetadata configuration and metadata ingestion scripts
- `src/openmetadata/sample_metadata/`: Business descriptions and user definitions

## Why OpenMetadata?
OpenMetadata was chosen for this implementation because it provides:
- Rich metadata management capabilities
- Built-in data discovery and exploration features
- Support for both technical and business metadata
- REST API for automation and integration
- Active open-source community

## Architecture

```mermaid
graph TD
A[Sample Data Scripts] -->|Loads| B[PostgreSQL DB]
B -->|Metadata Ingestion| C[OpenMetadata]
C -->|Serves| D[Web UI]
E[Schema/User Metadata] -->|Enriches| C
```

## Data Model
The system contains the following key schemas:

1. **real_estate_listings**: Core property listing data, photos, and location information
2. **sales**: Customer and transaction management
3. **marketing**: SEO, social media campaigns, and engagement tracking
4. **user_behaviour**: Website analytics and email engagement
5. **customer_support**: Support tickets and customer interactions
6. **real_estate_trackers**: Property search preferences and notifications
7. **czech_market_data**: Regional market statistics and trends
8. **location_amenities**: Nearby facilities and transport information
9. **human_resources**: Internal team management
10. **cloud_infrastructure**: System operations and costs

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Python 3.8+

### Installation & Setup

1. Create and start the OpenMetadata and PostgreSQL containers:

```bash
./1_create_openmetadata_and_database.sh
```

2. Configure the database connection in OpenMetadata:

```bash
./2_setup_database_connection.sh
```

3. Ingest the sample data:

```bash
./3_ingest_metadata.sh
```

4. Access the OpenMetadata UI at: http://localhost:8585
   - Username: admin@open-metadata.org
   - Password: admin

## Future Enhancements
- Implement Domains, Tiers, and Glossary
- Add data profiling
- Create data quality tests


