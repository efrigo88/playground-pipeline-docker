#!/bin/bash

# Stop containers first to ensure database is not in use
docker compose down

# Remove all files in psql-data directory
rm -rf psql-data/*

echo "All files in psql-data have been deleted"
