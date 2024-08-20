from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel



class UserInfo(BaseModel):
    uuid: UUID
    permissions: List = []

class ItemCreate(BaseModel):
    name: str
    description: str
    price: float
    quantity: int


class ItemRead(ItemCreate):
    id: int

    class Config:
        orm_mode = True


class ItemUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    quantity: Optional[int]
