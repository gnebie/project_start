# 
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Installer Poetry
RUN apt-get update \
    && apt-get install -y curl \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && apt-get clean


# Ajouter Poetry au PATH
ENV PATH="/root/.local/bin:$PATH"

# Créer et positionner le répertoire de l'application
WORKDIR /app


# Copier le fichier pyproject.toml et poetry.lock pour bénéficier du cache de Docker
COPY pyproject.toml poetry.lock* /app/

# Installer les dépendances du projet
RUN poetry install --no-root --no-dev

# Copier le reste du code de l'application
COPY . /app

# Installer les dépendances nécessaires à l'exécution de l'application
RUN poetry install --no-dev


# Exposer le port utilisé par l'application FastAPI
EXPOSE 80

# Commande pour lancer l'application FastAPI
CMD ["poetry", "run", "uvicorn", "{{ cookiecutter.project_name }}.__main__:app", "--host", "0.0.0.0", "--port", "80"]
