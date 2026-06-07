# slim is a minimal version of Debian with just enough
# to run Python — much smaller than the full image.
# AS base names this stage so other stages can build
# on top of it.
FROM python:3.14-slim AS base

# Sets the working directory inside the container.
WORKDIR /app

# apt-get update — refreshes the list of available packages
# apt-get install -y — installs packages without asking for confirmation
# gcc — C compiler, needed to compile psycopg2 from source
# libpq-dev — PostgreSQL development headers, also needed by psycopg2
# rm -rf /var/lib/apt/lists/* — cleans up the package list cache to keep the image size small
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
  && rm -rf /var/lib/apt/lists/*

COPY requirements/ requirements/

# =================
# DEV STAGE
# =================

# Starts a new stage that inherits everything from base.
# Named dev so docker-compose can target it specifically with target: dev.
FROM base AS dev
# Installs dev dependencies. --no-cache-dir tells pip not to cache downloaded packages.
RUN pip install --no-cache-dir -r requirements/dev.txt

# =================
# PROD STAGE
# =================

FROM base AS prod
RUN pip install --no-cache-dir -r requirements/prod.txt
