create-venv:
	@python -m venv venv

init-pre-commit: create-venv
	@echo "Starting git hooks ..."
	@echo "#!/bin/sh \nvenv/bin/pytest" > .git/hooks/pre-commit
	@chmod +x .git/hooks/pre-commit

setup-environment: init-pre-commit
	@echo "Creating the development environment ..."
	@venv/bin/pip install -q --upgrade pip
	@venv/bin/pip install -q --no-cache-dir -r requirements.dev.txt
	@venv/bin/pytest
	@echo "You finished ;)"

test:
	@venv/bin/pytest --cov

isort:
	@venv/bin/isort .

flake8:
	@venv/bin/flake8 app/ tests/

start:
	@venv/bin/uvicorn app.main:app --reload

docker:
	@docker-compose up -d
