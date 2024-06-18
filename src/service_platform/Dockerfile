# Use an official Python runtime as a parent image
FROM python:3.12.3-slim-bullseye as builder

# Set arguments
ARG POETRY_VERSION=1.8.3
ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_CREATE=1
ENV POETRY_VIRTUALENVS_IN_PROJECT=1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       libpq-dev \
       python3-dev \
       gcc \
       musl-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"

# Set the working directory in the container
WORKDIR /app

# Copy the pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock ./

# Install the dependencies using Poetry
RUN poetry install --no-root --without dev

# Use an official Python runtime as a parent image
FROM python:3.12.3-slim-bullseye as runtime

# Setup the Virtual Environment
ARG VIRTUAL_ENV=/app/.venv
COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

# Update the PATH environment
ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Copy the rest of the application code into the container
COPY src ./

# Expose port 8080
EXPOSE 8080

# Set environment variable
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "-m", "service_platform"]

# Run the application with Datadog tracing
# CMD ["ddtrace-run", "python", "-m", "service_platform"]
