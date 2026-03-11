# Variables
PYTHON=python
MANAGE=$(PYTHON) manage.py

# Default target
help:
	@echo "Available commands:"
	@echo "  make run        - Run development server"
	@echo "  make migrate    - Apply migrations"
	@echo "  make makemigrations - Create migrations"
	@echo "  make superuser  - Create superuser"
	@echo "  make shell      - Open Django shell"
	@echo "  make test       - Run tests"
	@echo "  make collectstatic - Collect static files"

run:
	$(MANAGE) runserver

migrate:
	$(MANAGE) migrate

makemigrations:
	$(MANAGE) makemigrations

update:
	$(MANAGE) makemigrations
	$(MANAGE) migrate

superuser:
	$(MANAGE) createsuperuser

shell:
	$(MANAGE) shell

test:
	$(MANAGE) test

collectstatic:
	$(MANAGE) collectstatic --noinput
