# SW Action Figure Co. Data Pipeline

## Project Overview
This project implements a data pipeline for SW Action Figure Co., which processes sales data of action figures, enriches it with external data from the Star Wars API (SWAPI), and loads the transformed data into a data warehouse for further analysis.

## Features
- Extracts sales data from a PostgreSQL source database.
- Enriches data with character details from the Star Wars API (SWAPI).
- Transforms data to include metrics like total revenue, quantity sold, and more.
- Loads the transformed data into a PostgreSQL data warehouse.
- Python application for easy setup and deployment.
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
- Python 3.9
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

3. **Initialize the databases**:
   The databases are automatically initialized with the required schemas when the PostgreSQL containers are first launched, using the SQL scripts mounted from `./app/sql/`.

## Usage

Once the Docker containers are running, the ETL process can be triggered by setting up a Python environment and running the pipeline script:

1. **Set up a Python virtual environment**:
   ```bash
   python3 -m venv sw-action-figure-co
   source sw-action-figure-co/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set the PYTHONPATH**:
   ```bash
   export PYTHONPATH=/path/to/your/project:$PYTHONPATH
   ```

4. **Run the data pipeline**:
   ```bash
   python app/data_pipeline.py
   ```

5. **Run the FastAPI application**:
   ```bash
   uvicorn app.main:app --reload
   ```
   Open your web browser and navigate to `localhost:8000/docs` to view the API documentation and interact with the API.

## Architecture

- **Data Extraction**: Data is extracted from the `db_source` PostgreSQL database using queries defined in the `extract_source_data` function in `app/utilities/etl.py`.
- **Data Transformation**: Data is enriched and transformed using both internal business logic and external data fetched from SWAPI. The transformation logic is implemented in the `transform_data` function.
- **Data Loading**: The transformed data is loaded into the `db_dw` PostgreSQL database, structured for analytical queries.

## CI/CD

GitHub Actions is used to automate the linting, testing, and deployment of the Docker container to GitHub Container Registry. The workflow is defined in `.github/workflows/main.yml`.

## Contributing

Contributions to this project are welcome. Please ensure that any pull requests pass the automated tests and conform to the coding standards set forth in the project.