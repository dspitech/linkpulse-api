FROM python:3.12-slim
WORKDIR /app
# curl est necessaire pour les healthchecks Docker Compose et Terraform
# upgrade applique les correctifs de securite Debian deja publies au moment du build
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*
# Etape 1 : copier uniquement le fichier de dependances
# Cette couche est mise en cache tant que requirements.txt ne change pas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Etape 2 : copier le code source (invalide a chaque modification)
COPY src/ ./src/
COPY tests/ ./tests/
EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
