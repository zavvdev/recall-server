DEV_COMPOSE = docker compose -f docker-compose.dev.yml
PROD_COMPOSE = docker compose -f docker-compose.prod.yml

# Creates virtual env folder
setup:
	python -m venv .venv

lint:
	$(DEV_COMPOSE) exec web ruff check . --fix

format:
	$(DEV_COMPOSE) exec web ruff format .

# ========================
# DEV
# ========================

# Build images without starting anything.
dev\:build:
	$(DEV_COMPOSE) build

# Start all containers.
dev\:start:
	$(DEV_COMPOSE) up

# Stops and removes the containers but keeps the volumes.
dev\:stop:
	$(DEV_COMPOSE) down

# Stops and removes the containers and volumes.
dev\:nuke:
	$(DEV_COMPOSE) down -v

# Create a migration for specific app.
dev\:make-migration:
	$(DEV_COMPOSE) exec web python manage.py makemigrations $(app)

# Run all migrations.
dev\:migrate:
	$(DEV_COMPOSE) exec web python manage.py migrate

# Create new module (app).
dev\:module:
	$(DEV_COMPOSE) exec web python manage.py startapp $(name)

# ========================
# PROD
# ========================

prod\:build:
	$(PROD_COMPOSE) build

# Start in detached mode.
prod\:start:
	$(PROD_COMPOSE) up -d

prod\:stop:
	$(PROD_COMPOSE) down

prod\:nuke:
	$(PROD_COMPOSE) down -v

prod\:make-migration:
	$(PROD_COMPOSE) exec web python manage.py makemigrations $(app)

prod\:migrate:
	$(PROD_COMPOSE) exec web python manage.py migrate

prod\:module:
	$(PROD_COMPOSE) exec web python manage.py startapp $(name)
