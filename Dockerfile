# Use official Python image as base
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Create necessary directories
RUN mkdir -p /app/data/warehouse/raw

# Install uv using pip
RUN pip install uv

# Create and activate virtual environment
ENV VIRTUAL_ENV=/app/.venv
RUN uv venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy project files
COPY pyproject.toml .

# Install dependencies using uv
RUN uv pip install --no-cache -e .

# Copy the rest of the application
COPY . .

# Command to run the application
CMD ["python", "src/main.py"]
