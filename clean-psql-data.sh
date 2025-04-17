#!/bin/bash

# Stop containers first to ensure database is not in use
docker compose down -v

# Remove all files in psql-data directory
find psql-data -mindepth 1 ! -name '.gitkeep' -delete

echo "All files in psql-data have been deleted"
