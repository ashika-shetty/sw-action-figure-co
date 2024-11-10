# SW Action Figure Co. Data Pipeline

## Project Overview
This project implements a data pipeline for SW Action Figure Co., which processes sales data of action figures, enriches it with external data from the Star Wars API (SWAPI), and loads the transformed data into a data warehouse for further analysis.

## Features
- Extracts sales data from a PostgreSQL source database.
- Enriches data with character details from the Star Wars API (SWAPI).
- Transforms data to include metrics like total revenue, quantity sold, and more.
- Loads the transformed data into a PostgreSQL data warehouse.
- Dockerized Python application for easy setup and deployment.
- Continuous Integration and Deployment with GitHub Actions.

## Technologies Used
- Python 3.9
- PostgreSQL
- Docker and Docker Compose
- GitHub Actions for CI/CD
- Libraries: Pandas, psycopg2-binary, httpx, requests

## Prerequisites
- Docker
- Docker Compose
- Git (optional, for cloning the repository)

## Setup Instructions

1. **Clone the repository** (optional if you have the files already):
   ```bash
   git clone https://github.com/ashika-shetty/sw-action-figure-co.git
   cd sw-action-figure-co
   ```

2. **Build and run the Docker containers**:
   ```bash
   docker-compose up --build
   ```
   This command builds the Docker image for the application and starts the necessary services defined in `docker-compose.yml`:
   - `db_source`: PostgreSQL database acting as the source of sales data.
   - `db_dw`: PostgreSQL database acting as the data warehouse.
   - `app`: Python application that runs the ETL process.

3. **Initialize the databases**:
   The databases are automatically initialized with the required schemas when the PostgreSQL containers are first launched, using the SQL scripts mounted from `./app/sql/`.

## Usage

Once the Docker containers are running, the ETL process can be triggered by executing the following command:
```bash
docker-compose exec app python app/data_pipeline.py
```

This command runs the `data_pipeline.py` script inside the `app` container, which performs the ETL operations.

## Architecture

- **Data Extraction**: Data is extracted from the `db_source` PostgreSQL database using queries defined in the `extract_source_data` function in `app/utilities/etl.py`.
- **Data Transformation**: Data is enriched and transformed using both internal business logic and external data fetched from SWAPI. The transformation logic is implemented in the `transform_data` function.
- **Data Loading**: The transformed data is loaded into the `db_dw` PostgreSQL database, structured for analytical queries.

## CI/CD

GitHub Actions is used to automate the linting, testing, and deployment of the Docker container to GitHub Container Registry. The workflow is defined in `.github/workflows/main.yml`.

## Contributing

Contributions to this project are welcome. Please ensure that any pull requests pass the automated tests and conform to the coding standards set forth in the project.