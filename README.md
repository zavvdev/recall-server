# Recall

Server application for Recall App. Create decks, flip cards, and build lasting memory through daily practice.

## Bootstrap

Setup [Python](./PYTHON_SETUP.md) in order to start developing.

[Docker](https://www.docker.com/) should be installed.

1. Create `.env.dev` and `.env.prod` files from examples.

2. Run `make setup` in order to create a virtual environment.

3. Run `make dev:build` in order to build docker images.

4. Run `make dev:start` in order to start all containers.

Admin panel will be accessible on `localhost:8000/admin`. Credentials are inside `.env.dev.example`.
Database will be accessible on `localhost:5432` with credentials from `.env.dev` file.

Check other commands in `Makefile`.
