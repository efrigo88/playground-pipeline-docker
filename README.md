# Data Pipeline with Docker

A data pipeline that fetches album data from JSONPlaceholder API, processes it using pandas, and stores it in PostgreSQL.

## Features

- Fetches album data from JSONPlaceholder API
- Processes and transforms data using pandas
- Stores data in PostgreSQL
- Containerized with Docker
- Environment variable configuration
- Logging system

## Project Structure

```
.
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose configuration
├── pyproject.toml          # Project dependencies and configuration
├── .env.example           # Example environment variables
└── src/
    ├── main.py            # Main pipeline script
    ├── api.py             # API client for JSONPlaceholder
    ├── db.py              # PostgreSQL database operations
    └── logger.py          # Logging configuration
```

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

## Setup

1. Copy the environment variables file:

   ```bash
   cp .env.example .env
   ```

2. Update the `.env` file with your PostgreSQL credentials:

   ```
   DB_HOST=localhost
   DB_PORT=5432
   DB_USER=your_user
   DB_PASSWORD=your_password
   DB_NAME=your_database
   ```

3. Build and run the Docker container:
   ```bash
   docker compose up -d --build
   ```

## Development

### Dependencies

- Python 3.9+
- pandas 2.2.0
- psycopg2-binary 2.9.9
- python-dotenv 1.0.0
- requests 2.31.0

### Development Dependencies

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
