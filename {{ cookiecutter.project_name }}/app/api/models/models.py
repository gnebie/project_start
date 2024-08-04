from sqlmodel import SQLModel, Field
from .base_class import Base


class Item(Base):
    __tablename__ = "item_example"

    name: str = Field(nullable=False)
    description: str = Field(nullable=True)
    price: float = Field(nullable=False)
    quantity: int = Field(default=0)