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
│   ├── api.py            # FastAPI endpoints
│   ├── client.py         # JSONPlaceholder API client
│   ├── db.py             # Database operations
│   ├── logger.py         # Logging configuration
│   ├── main.py           # Application entry point
│   └── pipeline.py       # Pipeline logic
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

## Running the Application

Start the application:

```bash
docker compose up -d
```

This will:

1. Start the FastAPI server
2. Start the PostgreSQL database
3. The API will be available at `http://localhost:8000`

### Triggering the Pipeline via API

You can trigger the pipeline to run using the API endpoint:

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

The application provides a REST API with the following endpoint:

- `POST /trigger-pipeline`: Triggers the data pipeline to run
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

## Pipeline Process

When triggered, the pipeline will:

1. Fetch album data from JSONPlaceholder API
2. Save raw data to the warehouse's raw layer
3. Transform the data (rename columns, add timestamps, etc.)
4. Save transformed data to the warehouse's bronze layer
5. Store the data in PostgreSQL

## Development

For local development:

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
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
