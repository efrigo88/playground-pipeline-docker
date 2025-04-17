# Playground Pipeline Docker

A data pipeline using PySpark, Iceberg, and PostgreSQL, containerized with Docker for easy deployment and development.

## Features

- PySpark for distributed data processing
- PostgreSQL for data storage
- Apache Iceberg for table format
- Dockerized environment for consistent development and deployment
- Pre-commit hooks for code quality
- Development tools configuration (black, isort, pytest)

## Prerequisites

- Docker and Docker Compose
- Python 3.9+ (for local development)
- Java 11 (for local Spark development)

## Project Structure

```
.
├── data/               # Data directory mounted in container
├── src/               # Source code
├── .env.example       # Example environment variables
├── .pre-commit-config.yaml  # Pre-commit hooks configuration
├── docker-compose.yml # Docker Compose configuration
├── Dockerfile         # Docker image definition
├── pyproject.toml     # Python project configuration
└── README.md          # Project documentation
```

## Environment Variables

Create a `.env` file based on `.env.example`:

```bash
# Spark basic configuration
SPARK_MASTER=local[4]
SPARK_DRIVER_MEMORY=8g
SPARK_SHUFFLE_PARTITIONS=4

# Postgres database credentials
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=postgres
```

## Getting Started

### Using Docker (Recommended)

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd playground-pipeline-docker
   ```

2. Copy the environment file:

   ```bash
   cp .env.example .env
   ```

3. Start the services:
   ```bash
   docker-compose up
   ```

The pipeline will be available and the PostgreSQL database will be running.

### Local Development

1. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   pip install -e ".[dev]"
   ```

3. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Development Tools

- **Black**: Code formatting
- **isort**: Import sorting
- **pytest**: Testing framework
- **pre-commit**: Git hooks for code quality

## Docker Services

### Pipeline Service

- Builds from the local Dockerfile
- Mounts the data directory
- Depends on the PostgreSQL service
- Restarts unless explicitly stopped

### PostgreSQL Service

- Uses PostgreSQL 17.4
- Persists data in `psql-data` directory
- Exposes port 5432
- Includes health checks
- Always restarts for reliability

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the terms of the LICENSE file in the root of this repository.
