from typing import List, Type, TypeVar
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.crud.crud import CRUDBase
from app.api.db.init_db import get_async_session

ModelType = TypeVar("ModelType", bound=SQLModel)

async def generate_crud_routes(model: Type[ModelType], schema: Type[BaseModel]) -> APIRouter:
    """
    Generate CRUD routes for a given SQLAlchemy model and Pydantic schema.

    Args:
        model (Type[ModelType]): SQLAlchemy model class.
        schema (Type[BaseModel]): Pydantic schema class.

    Returns:
        APIRouter: FastAPI router with CRUD routes.
    """
    genericRouter = APIRouter()
    crud_instance = CRUDBase[model, schema, schema](model)

    @genericRouter.post(f"/{model.__tablename__}/", response_model=schema)
    async def create_item(item: schema, db: AsyncSession = Depends(get_async_session)):
        """
        Create a new item in the database.

        Args:
            item (schema): Pydantic schema instance for the item to create.
            db (AsyncSession): SQLAlchemy async database session.

        Returns:
            schema: The created item.
        """
        return await crud_instance.create_async(db, item)

    @genericRouter.get(f"/{model.__tablename__}", response_model=List[schema])
    async def get_all_items(page: int = 1, page_size: int = 10, db: AsyncSession = Depends(get_async_session)):
        """
        Get a paginated list of items from the database.

        Args:
            page (int, optional): The page number to retrieve. Defaults to 1.
            page_size (int, optional): The number of items per page. Defaults to 10.
            db (AsyncSession): SQLAlchemy async database session.

        Returns:
            List[schema]: A list of items.
        """
        return await crud_instance.filter_and_paginate_async(db, page=page, page_size=page_size)

    @genericRouter.get(f"/{model.__tablename__}/{{item_id}}", response_model=schema)
    async def read_item(item_id: int, db: AsyncSession = Depends(get_async_session)):
        """
        Retrieve an item by its ID.

        Args:
            item_id (int): The ID of the item to retrieve.
            db (AsyncSession): SQLAlchemy async database session.

        Raises:
            HTTPException: If the item is not found.

        Returns:
            schema: The retrieved item.
        """
        db_item = await crud_instance.get_async(db, item_id)
        if db_item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return db_item

    @genericRouter.put(f"/{model.__tablename__}/{{item_id}}", response_model=schema)
    async def update_item(item_id: int, item: schema, db: AsyncSession = Depends(get_async_session)):
        """
        Update an item by its ID.

        Args:
            item_id (int): The ID of the item to update.
            item (schema): The updated item data.
            db (AsyncSession): SQLAlchemy async database session.

        Raises:
            HTTPException: If the item is not found.

        Returns:
            schema: The updated item.
        """
        db_item = await crud_instance.get_async(db, item_id)
        if db_item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return await crud_instance.update_async(db, db_item, item)

    @genericRouter.delete(f"/{model.__tablename__}/{{item_id}}", response_model=schema)
    async def delete_item(item_id: int, db: AsyncSession = Depends(get_async_session)):
        """
        Delete an item by its ID.

        Args:
            item_id (int): The ID of the item to delete.
            db (AsyncSession): SQLAlchemy async database session.

        Raises:
            HTTPException: If the item is not found.

        Returns:
            schema: The deleted item.
        """
        db_item = await crud_instance.get(db, item_id)
        if db_item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return await crud_instance.remove_async(db, item_id)

    return genericRouter

# Exemple de génération des routes pour un modèle User
# user_router = await generate_crud_routes(UserModel, UserSchema)
# app.include_router(user_router)