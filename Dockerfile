# Use official Python image as base
FROM python:3.9-slim

# Install Java for PySpark and other build dependencies
RUN apt-get update && \
    apt-get install -y \
    openjdk-11-jdk \
    curl \
    gcc \
    python3-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set Java environment variables
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# Set working directory
WORKDIR /app

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Copy project files
COPY pyproject.toml .

# Install dependencies using uv
RUN uv pip install --no-cache -e .

# Copy the rest of the application
COPY . .

# Command to run the application
CMD ["python", "src/main.py"]
