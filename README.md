# Data Pipeline with Docker

This project implements a data pipeline that fetches album data from the JSONPlaceholder API, processes it, and stores it in a PostgreSQL database. The entire pipeline runs in Docker containers and provides an API endpoint to trigger the pipeline.

## Prerequisites

- Docker and Docker Compose installed
- Python 3.8+ (for local development)

## Project Structure

```
.
├── data/                   # Data directory
│   └── warehouse/         # Data warehouse layers
│       ├── raw/          # Raw data
│       └── bronze/       # Processed data
├── src/                   # Source code
│   ├── api.py            # API client
│   ├── db.py             # Database operations
│   ├── logger.py         # Logging configuration
│   └── main.py           # Main pipeline
├── docker-compose.yml    # Docker Compose configuration
├── Dockerfile            # Pipeline container definition
├── .env                  # Environment variables
└── clean-psql-data.sh    # Database cleanup script
```

## Setup

1. Clone the repository
2. Create a `.env` file with the following variables:
   ```
   DB_HOST=postgres
   DB_PORT=5432
   DB_USER=postgres
   DB_PASSWORD=postgres
   DB_NAME=postgres
   ```

## Running the Pipeline

Start the pipeline:

```bash
docker compose up -d
```

The pipeline will:

1. Start the FastAPI server
2. Automatically run the pipeline once on startup
3. Keep running to accept API requests for additional pipeline runs

### Triggering the Pipeline via API

You can trigger the pipeline to run again using the API endpoint:

```bash
curl -X POST http://localhost:8000/trigger-pipeline
```

The API will return:

- Success response (200):
  ```json
  {
    "status": "success",
    "message": "Pipeline completed successfully"
  }
  ```
- Error response (500) if something goes wrong

## API Features

The pipeline provides a REST API with the following endpoint:

- `POST /trigger-pipeline`: Triggers the data pipeline to run
  - Automatically runs on container startup
  - Can be triggered multiple times while containers are running
  - Returns success/error status and message

## Database Management

### Accessing the Database

You can connect to the PostgreSQL database using:

```bash
docker compose exec postgres psql -U postgres
```

### Cleaning Database Data

To delete all database files and start fresh:

```bash
./clean-psql-data.sh
```

This script will:

- Stop all running containers
- Delete all files in the `psql-data` directory
- Print a confirmation message

## Development

For local development without Docker:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python src/main.py
```

## Features

- Fetches album data from JSONPlaceholder API
- Processes and transforms data using pandas
- Stores data in PostgreSQL
- Containerized with Docker
- Environment variable configuration
- Logging system

## Data Flow

1. Fetch album data from JSONPlaceholder API
2. Save raw data to JSON file
3. Transform data:
   - Convert data types
   - Rename columns
   - Add ingestion timestamp
4. Store processed data in PostgreSQL

## Data Schema

### Albums Table

| Column              | Type      | Description                       |
| ------------------- | --------- | --------------------------------- |
| album_id            | INTEGER   | Unique identifier for the album   |
| user_id             | INTEGER   | ID of the user who owns the album |
| album_title         | TEXT      | Title of the album                |
| ingestion_timestamp | TIMESTAMP | When the record was processed     |

## Development Dependencies

- pytest
- black
- isort
- pre-commit
- pylint

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black .
isort .
```

## License

MIT
