"""
Module for permission verification middleware and route example.

This module includes functions to verify user permissions by
communicating with the login API and an example route demonstrating
the use of the middleware.
"""

import httpx
from app.config import settings
from app.api.schemas.schemas import UserInfo
from fastapi import Depends, HTTPException, status, Request
from typing import List
from enum import Enum as PyEnum
import logging

logger = logging.getLogger(__name__)


class PermissionError(Exception):
    """Custom exception for permission errors."""

    pass


def get_token(request: Request) -> str:
    """Extract the Bearer token from the request headers.

    Args:
        request (Request): The FastAPI request object.

    Returns:
        str: The extracted token.

    Raises:
        HTTPException: If the Authorization header is missing or invalid.
    """
    logger.trace("Get user token")
    bearer = "Bearer "
    authorization: str = request.headers.get("Authorization")
    if not authorization or not authorization.startswith(bearer):
        logger.debug("User authorization token Not found")
        logger.trace(request)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing authorization token",
        )
    return authorization[len(bearer) :]


def verfy_permissions(user_permissions, required_permissions, system="any"):
    if system == "any":
        # all permission system
        if not any(perm in user_permissions for perm in required_permissions):
            logger.warn("invalid any user permissions")
            logger.debug(f"invalid user permissions required permissions: {required_permissions} user permissions :{user_permissions}")

            raise HTTPException(status_code=403, detail="Not enough permissions")
            # raise PermissionError(f"Missing permissions: {required_permissions}")
    if system == "all":
        # all permission system
        if not all(perm in user_permissions for perm in required_permissions):
            logger.warn("invalid all user permissions")
            logger.debug(f"invalid user permissions required permissions: {required_permissions} user permissions :{user_permissions}")

            raise HTTPException(status_code=403, detail="Not enough permissions")
            # raise PermissionError(f"Missing permissions: {required_permissions}")


def get_user_and_verify_permissions(required_permissions: List[str]):
    """Dependency function to verify user permissions via the login API.

    Args:
        required_permissions (List[str]): List of permissions required for the route.

    Returns:
        Callable: A dependency function that verifies user permissions.

    Raises:
        HTTPException: If the credentials are invalid.
        PermissionError: If the user lacks required permissions.
    """

    async def _get_user_and_verify_permissions(token: str = Depends(get_token)) -> List[str]:
        """Inner function to perform the actual permission verification.

        Args:
            token (str): The Bearer token extracted from the request headers.

        Returns:
            List[str]: List of user permissions.

        Raises:
            HTTPException: If the login API response is not successful.
            PermissionError: If the user does not have all required permissions.
        """
        logger.trace("Call user manager api with the user token")

        async with httpx.AsyncClient() as client:
            response = await client.post(
                settings.LOGIN_API_URL + "/verify-permission",
                headers={"Authorization": f"Bearer {token}"},
            )
            logger.debug(f"Api return status code {response.status_code} ")

            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Could not validate credentials",
                )
            user = response.json()
            permissions = user.get("permissions", [])
            logger.trace(f"user {user} ")
            logger.debug(f"user permissions {permissions} ")
            verfy_permissions(permissions, required_permissions)

            return UserInfo(**user)

    return _get_user_and_verify_permissions


# a supprimer
def verify_permissions(required_permissions: List[str]):
    return get_user_and_verify_permissions(required_permissions)


def verify_permissions_short(shortcut_permission: str):
    logger.info(f" verify permissions {shortcut_permission}")
    logger.debug(f"permissions {permissions_shortcut.get(shortcut_permission,[])} ")
    return get_user_and_verify_permissions(permissions_shortcut.get(shortcut_permission, []))


class Permissions(PyEnum):
    CrudUsers = "CRUD Users"


permissions_shortcut = {
    Permissions.CrudUsers: [
        "CreateMyInfos",
        "GetMyInfos",
        "UpdateMyInfos",
        "DeleteMyInfos",
    ],
}
