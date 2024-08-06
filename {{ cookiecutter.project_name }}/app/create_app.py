import logging
from fastapi import FastAPI, Depends
from fastapi_pagination import add_pagination
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.openapi.utils import get_openapi
import json
from contextlib import asynccontextmanager

from app.config.logger import setup_logging
from app.api.db import async_init_db
from app.config.settings import settings
from app.middleware import TraceIDMiddleware
from app.middleware import PrometheusMiddleware

# from app.middleware import firebase_auth
from app.metrics import start_prometheus_server
from app.api.v1 import add_routes

from icecream import ic

# Configure logger
logger = logging.getLogger(__name__)


app = FastAPI(
    title="API",
    description="The API microservice",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "",
            "description": "Operations with .",
        },
    ],
)


def add_middlewares_catch_global_error(middleware_name, middleware_add_function):
    try:
        # Add monitoring middleware
        logger.trace("Adding middleware : " + middleware_name)
        middleware_add_function()
    except Exception as e:
        ic(e)
        logger.error("Error adding middlewares : " + middleware_name, exc_info=True)


def add_middlewares(settings, app):
    """
    Add middlewares to the FastAPI application.

    :param settings: Application settings
    :param app: FastAPI application instance
    """
    logger.info("Adding middlewares to the FastAPI application")
    add_middlewares_catch_global_error("PrometheusMiddleware", lambda: app.add_middleware(PrometheusMiddleware))
    add_middlewares_catch_global_error(
        "CORSMiddleware",
        lambda: app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Adjust allowed origins
            allow_credentials=True,
            allow_methods=["GET", "POST", "PUT", "DELETE"],
            allow_headers=["*"],
        ),
    )
    add_middlewares_catch_global_error("HTTPSRedirectMiddleware", lambda: app.add_middleware(HTTPSRedirectMiddleware))
    add_middlewares_catch_global_error("TraceIDMiddleware", lambda: app.add_middleware(TraceIDMiddleware))
    # add_middlewares_catch_global_error("TraceIDMiddleware", lambda: app.add_middleware(firebase_auth))


def init_services(settings):
    """
    Initialize external services for the FastAPI application.

    :param settings: Application settings
    """
    if settings.ENV.lower() == "test" or settings.ENV.lower() == "dev":
        return
    logger.info("Initializing external services")
    try:
        # Start the Prometheus server
        start_prometheus_server(settings)
    except Exception as e:
        ic(e)
        logger.error("Error initializing services", exc_info=True)


def create_app():
    """
    Application startup event handler.

    This function initializes the database, services, middlewares, routes,
    and adds pagination to the FastAPI application.

    :param settings: Application settings
    :return: FastAPI application instance
    """
    # ic(settings)
    try:
        logger.info("Starting up the FastAPI application")
        add_middlewares(settings, app)
        init_services(settings)
        add_routes(settings, app)
        add_pagination(app)
        return app
    except Exception as e:
        ic(e)
        logger.error("Error during app startup", exc_info=True)


async def generate_openapi():
    pathfile = "docs/openapi.json"
    openapi_schema = get_openapi(
        title=settings.PROJECT_NAME,
        version="1.0.0",
        description="API Description",
        routes=app.routes,
    )
    logger.trace("Create the last openapi schema the FastAPI application")
    try:
        with open(pathfile, "w") as file:
            json.dump(openapi_schema, file, indent=4)
    except Exception as e:
        ic(e)
        logger.error("Error during Openapi creation : " + pathfile, exc_info=True)


@asynccontextmanager
async def on_startup(app: FastAPI):
    # Actions à effectuer au démarrage
    await async_init_db()
    await generate_openapi()
    yield


app = FastAPI(lifespan=on_startup)
app = create_app()
