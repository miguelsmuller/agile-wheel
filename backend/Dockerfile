# Use Python 3.12 slim as the base image
FROM python:3.12.0-slim

# Set the working directory
WORKDIR /app

# Copy Poetry configuration files
COPY pyproject.toml poetry.lock ./

# Install Poetry for dependency management
RUN pip install --no-cache-dir poetry

# Copy the README file
COPY README.md .

# Copy the source code
COPY src ./src

# Configure Poetry to not create virtual environments
RUN poetry config virtualenvs.create false

# Install dependencies using Poetry
RUN poetry install --no-interaction --no-ansi

# Set the internal port environment variable
ENV INTERNAL_PORT=8000

# Expose the internal port
EXPOSE ${INTERNAL_PORT}

# Copy the entrypoint script
COPY entrypoint.sh /entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /entrypoint.sh

# Set the entrypoint script
ENTRYPOINT ["/entrypoint.sh"]