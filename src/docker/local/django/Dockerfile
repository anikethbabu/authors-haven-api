#Setup python version in PYTHON_VERSION variable for build processes
ARG PYTHON_VERSION=3.11.2-bullseye

FROM python:${PYTHON_VERSION} as python

# Build stage 1. Building python dependency wheels in this stage.
FROM python as python-build-stage
ARG BUILD_ENVIRONMENT=local

# Update and install specified packages without having to install recommended packages
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev

# Copy requirements from host machine to folder
COPY ./requirements .

# Specifies to store dependency wheels in /usr/src/app/wheels and downloads requirements.txt in wheels directory
RUN pip wheel --wheel-dir /usr/src/app/wheels \
    -r ${BUILD_ENVIRONMENT}.txt

# Build stage 2. Running  
FROM python as python-run-stage
ARG BUILD_ENVIRONMENT=local

# Setting where the application code will be store in container
ARG APP_HOME=/app

# Tell python to stop writing .pyc files.
ENV PYTHONDONTWRITEBYTECODE 1

# Python output is transmitted to terminal without being buffered. Displays application output in real time.
ENV PYTHONUNBUFFERED 1

ENV BUILD_ENVIRONMENT ${BUILD_ENVIRONMENT}

# Sets working directory for any run, cmd, entrypoint, copy, and add instructions after it in the Dockerfile
WORKDIR ${APP_HOME}

# Updates and downloads dependencies. 
RUN apt-get update && apt-get install --no-install-recommends -y \
    libpq-dev \
    gettext \
    # Removes uncessary files, package cache, and configuration with purge and also remove installed packages no longer needed with --auto-remove.
    && apt-get purge -y --auto-remove -o \
    # Sets autoremove to delete and cleanup files that are Recommended important.
    APT::AutoRemove::RecommendsImportant=false \
    # Removes package index files no longer needed once packages are installed. Reduces docker image size.
    && rm -rf /var/lib/apt/lists/*

# From build stage 1 install the wheels to wheels directory.
COPY --from=python-build-stage /usr/src/app/wheels /wheels/

# Installs wheels via pip and avoids creating package cache. --no-index stops pip from searching pypi for packages. --find-links find /wheels/ directory.
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
    # After installing wheels delete wheels
    && rm -rf /wheels/

COPY ./docker/local/django/entrypoint /entrypoint
# Ensures /entrypoint has unix style line endings. Substitutes carriage return character at end of the line with empty string globally.
RUN sed -i 's/\r$//g' /entrypoint
# Ensure /entrypoint can be executed to be started properly.
RUN chmod +x /entrypoint

COPY ./docker/local/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY ./docker/local/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY ./docker/local/django/celery/flower/start /start-flower
RUN sed -i 's/\r$//g' /start-flower
RUN chmod +x /start-flower


COPY . ${APP_HOME}

# Defines primary command the container will execute at launch
ENTRYPOINT [ "/entrypoint" ]
