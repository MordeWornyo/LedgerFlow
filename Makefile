.PHONY: up down restart build rebuild logs ps clean lint test setup test-docker coverage verify

up:
	docker compose up -d

down:
	docker compose down -v --remove-orphans

restart:
	docker compose down -v --remove-orphans
	docker compose up -d

build:
	docker compose build

rebuild:
	docker compose down -v --remove-orphans
	docker compose build --no-cache
	docker compose up -d

logs:
	docker compose logs -f

ps:
	docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

clean:
	docker compose down -v --remove-orphans
	docker system prune -a --volumes -f

setup:
	python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt -r requirements-dev.txt

lint:
	ruff check .

test:
	pytest -v --cov=. --cov-report=term-missing

# Run tests inside Dockerized environment (isolated CI flow)
test-docker:
	docker compose up -d
	docker compose run --rm test-runner pytest -v --cov=. --cov-report=term-missing
	docker compose down -v --remove-orphans

# Generate full HTML coverage report (in Docker)
coverage:
	docker compose up -d
	docker compose run --rm test-runner pytest --cov=. --cov-report=html
	@echo "\nCoverage report generated at htmlcov/index.html"
	docker compose down -v --remove-orphans

# Combined check: lint + docker tests
verify: lint test-docker
	@echo "\nAll checks passed successfully!"
