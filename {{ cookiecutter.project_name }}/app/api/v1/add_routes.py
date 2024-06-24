from icecream import ic

logger = logging.getLogger(__name__)
def add_routes(settings, app):
    """
    Add routes to the FastAPI application.

    :param settings: Application settings
    :param app: FastAPI application instance
    """
    logger.trace("Adding routes to the FastAPI application")
    try:
        pass
        # Unprotected routes
        # app.include_router(public_router.get_public_router(), prefix="/api/v1")
        # Global unprotected routes
        # app.include_router(global_router.get_global_router(), prefix="/api")
        # Protected user routes
        # app.include_router(user_router.get_user_router(), prefix="/api/v1/user", tags=["User"])
        # app.include_router(user_router.get_user_router(), prefix="/api/v1/user", tags=["User"], dependencies=[Depends(firebase_auth)])
        # Protected admin routes
        # app.include_router(admin_router.get_admin_router(), prefix="/api/v1/admin", tags=["Admin"], dependencies=[Depends(firebase_auth)])
    except Exception as e:
        ic(e)
        logger.error("Error adding routes", exc_info=True)
