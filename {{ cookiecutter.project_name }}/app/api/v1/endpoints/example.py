from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.schemas.item import ItemCreate, ItemRead, ItemUpdate
from app.models.item import Item
from app.db.session import get_session
from app.crud.base import CRUDBase
from fastapi_pagination import Page, add_pagination, Params

router = APIRouter()
crud_item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)

async def get_routes_example():
    @router.post("/", response_model=ItemRead, dependencies=[Depends(firebase_auth)])
    async def create_item(item_in: ItemCreate, db: AsyncSession = Depends(get_session)):
        return await crud_item.create_async(db, item_in)

    @router.get("/{id}", response_model=ItemRead, dependencies=[Depends(firebase_auth)])
    async def read_item(id: int, db: AsyncSession = Depends(get_session)):
        item = await crud_item.get_async(db, id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return item

    @router.put("/{id}", response_model=ItemRead, dependencies=[Depends(firebase_auth)])
    async def update_item(id: int, item_in: ItemUpdate, db: AsyncSession = Depends(get_session)):
        item = await crud_item.get_async(db, id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return await crud_item.update_async(db, item, item_in)

    @router.delete("/{id}", response_model=ItemRead, dependencies=[Depends(firebase_auth)])
    async def delete_item(id: int, db: AsyncSession = Depends(get_session)):
        item = await crud_item.remove_async(db, id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return item

    @router.get("/filter", response_model=Page[ItemRead], dependencies=[Depends(firebase_auth)])
    async def filter_items(
        name: Optional[str] = Query(None),
        price: Optional[float] = Query(None),
        select_fields=["name", "price"],
        order_by: Optional[str] = Query(None),
        ascending: bool = Query(True),
        db: AsyncSession = Depends(get_session),
        params: Params = Depends(),
        request: Request
    ):
        await firebase_auth.check_role(request, "user")
        filters = {}
        if name:
            filters["name"] = name
        if price:
            filters["price"] = price
        return await crud_item.filter_and_paginate_async(db, filters, order_by=order_by, ascending=ascending, select_fields=select_fields)

    add_pagination(router)