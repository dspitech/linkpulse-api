IMAGE_NAME = linkpulse-api
PORT       = 8000

.PHONY: build run stop test lint clean tag

build:
	docker build -t $(IMAGE_NAME):latest .

run:
	docker compose up -d

stop:
	docker compose down

# Lance les tests DANS le conteneur Docker (même environnement qu'en CI)
test:
	docker run --rm \
		-v $(PWD):/app \
		-w /app \
		$(IMAGE_NAME):latest \
		pytest tests/ -v --cov=src --cov-report=term-missing

lint:
	docker run --rm \
		-v $(PWD):/app \
		-w /app \
		python:3.12-slim \
		sh -c "pip install flake8 -q && flake8 src/ --max-line-length=100"

clean:
	docker compose down -v
	docker rmi $(IMAGE_NAME):latest || true

tag:
	git tag -a v0.1.0 -m "Premiere version LinkPulse"
	git push origin v0.1.0
