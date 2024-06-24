import logging
from fastapi import FastAPI, Depends
from fastapi_pagination import add_pagination
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.openapi.utils import get_openapi
import json
from contextlib import asynccontextmanager

from app.config.logger import setup_logging
from app.api.db.init_db import async_init_db
from app.config.settings import settings
from app.middleware import TraceIDMiddleware
from app.middleware import PrometheusMiddleware
from app.middleware import firebase_auth
from app.metrics import start_prometheus_server
# from app.api.v1.endpoints import user_router, admin_router, public_router, global_router
from app.api.v1 import add_routes

from icecream import ic

# Configure logger
logger = logging.getLogger(__name__)


app = FastAPI(
    title="User API",
    description="The User API microservice",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "users",
            "description": "Operations with users.",
        },
    ],
)

def add_middlewares(settings, app):
    """
    Add middlewares to the FastAPI application.

    :param settings: Application settings
    :param app: FastAPI application instance
    """
    logger.trace("Adding middlewares to the FastAPI application")
    try:
        # Add monitoring middleware
        app.add_middleware(PrometheusMiddleware)
    except Exception as e:
        ic(e)
        logger.error("Error adding middlewares", exc_info=True)
    try:
        
        # CORS (Cross-Origin Resource Sharing) middleware
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Adjust allowed origins
            allow_credentials=True,
            allow_methods=["GET", "POST", "UPDATE", "DELETE"],
            allow_headers=["*"],
        )
    except Exception as e:
        ic(e)
        logger.error("Error adding middlewares", exc_info=True)
    try:
        # HTTPS redirect middleware
        app.add_middleware(HTTPSRedirectMiddleware)
    except Exception as e:
        ic(e)
        logger.error("Error adding middlewares", exc_info=True)
    try:
        # TraceID middleware: add a unique request ID to the log to trace requests through the logs
        app.add_middleware(TraceIDMiddleware)
    except Exception as e:
        ic(e)
        logger.error("Error adding middlewares", exc_info=True)
    # try:
    #     # Firebase authentication middleware
    #     app.add_middleware(firebase_auth)
    # except Exception as e:
    #     ic(e)
    #     logger.error("Error adding middlewares", exc_info=True)

def init_services(settings):
    """
    Initialize external services for the FastAPI application.

    :param settings: Application settings
    """
    logger.trace("Initializing external services")
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
        # setup_logging(log_folder=os.getenv('LOG_FOLDER', 'logs'), log_level=os.getenv('LOG_LEVEL', 'INFO'))
        # logger.trace("Starting up the FastAPI application")
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
    try:
        with open(pathfile, "w") as file:
            json.dump(openapi_schema, file, indent=4)
    except Exception as e:
        ic(e)
        logger.error("Error during Openapi creation : " + pathfile, exc_info=True)

# @app.on_event("startup")
# async def on_startup():
#     await async_init_db()
#     await generate_openapi()

@asynccontextmanager
async def on_startup(app: FastAPI):
    # Actions à effectuer au démarrage
    await async_init_db()
    await generate_openapi()
    yield

app = FastAPI(lifespan=on_startup)
app = create_app()