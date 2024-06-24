from pydantic import BaseModel

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