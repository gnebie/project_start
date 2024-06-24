.PHONY: init install-dev test build docs clean deploy lint format sphinx-start sphinx-build create-executable cookiecutter-run add add-from-requirements add-dev

# Variables
DOCKER_NAME={{ cookiecutter.project_name }}
PROJECT_NAME=app
DOCS_DIR=docs
PYINSTALLER_OPTS=--onefile cli.py
PORT=8000
INTERNALPORT=80

# Sphinx documentation
sphinx-start:
	sphinx-quickstart $(DOCS_DIR)

sphinx-build:
	(cd $(DOCS_DIR); make html)

# Initialization and installation of dependencies
init:
	poetry install --no-dev

install-dev:
	poetry install

# Run the application localy
local-run:
	poetry run uvicorn $(PROJECT_NAME).create_app:app --reload --ssl-keyfile=config-files/key.pem --ssl-certfile=config-files/cert.pem

# Build the executable
build:
	poetry run pyinstaller $(PYINSTALLER_OPTS)

# Running tests
test:
	poetry run pytest tests

# Running tests
test-coverage:
	poetry run pytest --cov=app --cov-report=xml --junitxml=tests/reports/results.xml

# Linting the code
lint:
	poetry run flake8 .

# Formatting the code
format:
	poetry run black .

# Clean generated files
clean:
	@rm -rf build dist *.spec
	@find . -type d -name "__pycache__" -exec rm -r {} +
	@find . -type d -name ".mypy_cache" -exec rm -r {} +
	@find . -type d -name ".pytest_cache" -exec rm -r {} +
	@rm -rf .coverage coverage.xml

# Deploy the application (example with Docker)
deploy:
	@docker build -t $(DOCKER_NAME) .
	@docker run -d -p $(PORT):$(INTERNALPORT) $(DOCKER_NAME)

# Create executable placeholder
create-executable:
	echo "see pyinstaller doc : pyinstaller --onefile cli.py"
	echo "https://realpython.com/pyinstaller-python/"

# Add a new dependency
add:
	@read -p "Enter the package name to add: " package; \
	poetry add $$package

# Add dependencies from requirements files
add-from-requirements:
	poetry add $(shell cat requirements.txt)
	poetry add --dev $(shell cat requirements-dev.txt)

# Add a new development dependency
add-dev:
	@read -p "Enter the development package name to add: " package; \
	poetry add --dev $$package

# SonarQube analysis
sonar:
	poetry run pytest --cov=app --cov-report=xml --junitxml=tests/reports/results.xml
	sonar-scanner