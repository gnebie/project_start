import os
import json
from typing import Any, Dict, Optional, Tuple, Type
from pathlib import Path
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, JsonConfigSettingsSource
from pydantic import  Field, field_validator, ValidationInfo, ConfigDict
from pydantic.fields import FieldInfo
import logging

logger = logging.getLogger(__name__)

environment = os.getenv('ENVIRONMENT', 'dev')
env_file = os.getenv('{{ cookiecutter.project_name }}_ENV_FILE', f'config-files/.env.{environment}')
config_file = os.getenv('{{ cookiecutter.project_name }}_CONFIG_FILE', f'config-files/config-{environment}.json')

class Settings(BaseSettings):
    """
    Configuration settings for the UserManager application.

    Attributes:
        PROJECT_NAME (str): The name of the project.
        ENV (str): The environment (e.g., 'prod', 'dev', 'test').
        DB_URL (str): The database URL.
        DB_USER (str): The database user.
        DB_PASSWORD (str): The database password.
        DB_HOST (str): The database host.
        DB_PORT (int): The database port.
        DB_NAME (str): The database name.
        PROMETHEUS_PORT (int): The port for Prometheus metrics.
        LOG_FOLDER (str): The folder where logs are stored.
        LOG_FILE (str): The log file name.
        LOG_LEVEL (str): The logging level.
        LOG_CONSOLE (str): The console log level.
        DRY_RUN (bool): If True, do not make actual API calls.
    """
    PROJECT_NAME: str = "UserManager"
    ENV: str = environment
    DB_URL: str = ""
    DB_DIALECT: str = "postgresql"
    DB_DRIVER: str = "asyncpg"
    DB_USER: str = ""
    DB_PASSWORD: str = ""
    DB_HOST: str = ""
    DB_PORT: int = 5432
    DB_NAME: str = ""
    PROMETHEUS_PORT: int = 8001
    LOG_FOLDER: str = "logs"
    LOG_FILE: str = "{{ cookiecutter.project_name }}.log"
    LOG_LEVEL: str = "INFO"
    LOG_CONSOLE: str = "TRACE"
    DRY_RUN: bool = False

    model_config = ConfigDict(env_file=env_file, env_file_encoding='utf-8')

    @classmethod
    def customise_sources(
        cls,
        init_settings,
        env_settings,
        dotenv_settings,
        file_secret_settings,
    ):
        return (
            init_settings,
            # JsonConfigSettingsSource(cls),
            env_settings,
            dotenv_settings,
            file_secret_settings,
        )

    @classmethod
    def from_json(cls, path: Optional[str] = None) -> "Settings":
        """
        Loads additional settings from a JSON configuration file.

        Args:
            config_file (str): The path to the JSON configuration file.

        Logs:
            Logs an error if the file is missing or cannot be read.
        """
        config = {}
        if path and os.path.exists(path):
            try:
                with open(path) as f:
                    config = json.load(f)
            except FileNotFoundError:
                logger.error(f"Configuration file {config_file} not found.")
            except json.JSONDecodeError:
                logger.error(f"Error decoding JSON from the configuration file {config_file}.")
        return cls(**config)


# Initialisation des paramètres
settings = Settings.from_json(config_file)
settings = Settings()
