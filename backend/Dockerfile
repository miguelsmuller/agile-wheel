# ******************
# Step 1 - Base
# ******************
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

# Start FastAPI server using Uvicorn
CMD ["sh", "-c", "poetry run uvicorn src.main:app --host 0.0.0.0 --port ${INTERNAL_PORT}"]