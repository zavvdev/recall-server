# Creates virtual env folder
setup:
	python -m venv .venv

lint:
	docker compose -f docker-compose.dev.yml exec web ruff check . --fix

format:
	docker compose -f docker-compose.dev.yml exec web ruff format .

# ========================
# DEV
# ========================

# Build images without starting anything.
dev\:build:
	docker compose -f docker-compose.dev.yml build

# Start all containers.
dev\:start:
	docker compose -f docker-compose.dev.yml up

# Stops and removes the containers but keeps the volumes.
dev\:stop:
	docker compose -f docker-compose.dev.yml down

# Stops and removes the containers and volumes.
dev\:nuke:
	docker compose -f docker-compose.dev.yml down -v

# Run migrations
dev\:migrate:
	docker compose -f docker-compose.dev.yml exec web python manage.py migrate

# Create new module (app)
dev\:module:
	docker compose -f docker-compose.dev.yml exec web python manage.py startapp $(name)

# ========================
# PROD
# ========================

prod\:build:
	docker compose -f docker-compose.prod.yml build

# Start in detached mode.
prod\:start:
	docker compose -f docker-compose.prod.yml up -d

prod\:stop:
	docker compose -f docker-compose.prod.yml down

prod\:nuke:
	docker compose -f docker-compose.prod.yml down -v

prod\:migrate:
	docker compose -f docker-compose.prod.yml exec web python manage.py migrate

prod\:module:
	docker compose -f docker-compose.prod.yml exec web python manage.py startapp $(name)

prod\:superu:
	docker compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
