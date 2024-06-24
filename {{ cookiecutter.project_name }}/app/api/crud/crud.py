from typing import Type, TypeVar, Generic, List, Optional, Union, Dict, Any
from sqlmodel import SQLModel, select
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import Page, paginate
from sqlalchemy.orm import joinedload
import logging
from fastapi import APIRouter, Depends, HTTPException, Query

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    CRUD (Create, Read, Update, Delete) base class providing generic methods for database operations.
    
    Attributes:
        model (Type[ModelType]): SQLAlchemy model class.
    """
        
    def __init__(self, model: Type[ModelType]):
        """
        Initialize the CRUD base class.
        
        Args:
            model (Type[ModelType]): SQLAlchemy model class.
        """
        self.model = model
        self.logger = logging.getLogger(self.model.__name__)

    async def get_async(self, db: AsyncSession, id: int) -> Optional[ModelType]:
        """
        Fetch a single record by ID asynchronously.
        
        Args:
            db (AsyncSession): The database session.
            id (int): The ID of the record to fetch.
            
        Returns:
            Optional[ModelType]: The record with the specified ID, or None if not found.
        """
        self.logger.debug(f"Fetching {self.model.__name__} with id: {id} asynchronously")
        result = await db.execute(select(self.model).where(self.model.id == id))
        return result.scalars().first()

    async def create_async(self, db: AsyncSession, obj_in: CreateSchemaType) -> ModelType:
        """
        Create a new record asynchronously.
        
        Args:
            db (AsyncSession): The database session.
            obj_in (CreateSchemaType): The data for the new record.
            
        Returns:
            ModelType: The created record.
        """
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        self.logger.debug(f"Creating {self.model.__name__} asynchronously with data: {obj_in_data}")
        try:
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
            return db_obj
        except IntegrityError as e:
            await db.rollback()
            self.logger.error(f"Error creating {self.model.__name__} asynchronously: {e}")
            raise

    async def update_async(self, db: AsyncSession, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
        """
        Update an existing record asynchronously.
        
        Args:
            db (AsyncSession): The database session.
            db_obj (ModelType): The existing record to update.
            obj_in (Union[UpdateSchemaType, Dict[str, Any]]): The new data for the record.
            
        Returns:
            ModelType: The updated record.
        """
        obj_data = obj_in.dict(exclude_unset=True) if isinstance(obj_in, BaseModel) else obj_in
        self.logger.debug(f"Updating {self.model.__name__} id: {db_obj.id} asynchronously with data: {obj_data}")
        for field in obj_data:
            setattr(db_obj, field, obj_data[field])
        try:
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
            return db_obj
        except IntegrityError as e:
            await db.rollback()
            self.logger.error(f"Error updating {self.model.__name__} asynchronously: {e}")
            raise

    async def remove_async(self, db: AsyncSession, id: int) -> Optional[ModelType]:
        """
        Remove a record by ID asynchronously.
        
        Args:
            db (AsyncSession): The database session.
            id (int): The ID of the record to remove.
            
        Returns:
            Optional[ModelType]: The removed record, or None if not found.
        """
        self.logger.debug(f"Removing {self.model.__name__} with id: {id} asynchronously")
        result = await db.execute(select(self.model).where(self.model.id == id))
        obj = result.scalars().first()
        if obj:
            await db.delete(obj)
            await db.commit()
        return obj

    async def filter_and_paginate_async(self, db: AsyncSession, filters: Dict[str, Any], 
        order_by: Optional[str] = None, 
        ascending: bool = True, 
        select_fields: Optional[List[str]] = None) -> Page[ModelType]:
        """
        Filter records by attributes and optionally select specific fields asynchronously.
        
        Args:
            db (AsyncSession): The database session.
            select_fields (Optional[List[str]]): The fields to select.
            order_by (Optional[str]): The field to order by.
            ascending (bool): Whether to sort in ascending order.
            filters: The filter criteria.
            
        Returns:
            Page[ModelType]: The filtered and paginated records.
        """
        self.logger.debug(f"Filtering {self.model.__name__} asynchronously with filters: {filters}")
        query = select(self.model)
        for attr, value in filters.items():
            query = query.filter(getattr(self.model, attr) == value)
        
        if select_fields:
            query = query.with_entities(*[getattr(self.model, field) for field in select_fields])
        
        if order_by:
            order_column = getattr(self.model, order_by)
            if ascending:
                query = query.order_by(order_column.asc())
            else:
                query = query.order_by(order_column.desc())
        
        return await paginate(db, query)