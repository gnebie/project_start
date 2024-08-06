from fastapi import APIRouter, Depends, HTTPException, Query
from app.config.version import version_1, get_versions
from starlette.requests import Request


def get_public_router():
    publicRouter = APIRouter()

    @publicRouter.get("/version", tags=["Public"], operation_id="public_router_version")
    async def getVersion():
        return {"version": version_1}

    @publicRouter.get("/helth", tags=["Public"], operation_id="public_router_helth")
    async def health():
        return {"status": "ok"}

    @publicRouter.get("/trace", tags=["Public"], operation_id="public_router_helth")
    async def trace(request: Request):
        return {"trace_id": request.state.trace_id}

    return publicRouter
