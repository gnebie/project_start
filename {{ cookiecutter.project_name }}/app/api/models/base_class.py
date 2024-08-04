from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import UniqueConstraint
from typing import Optional, List
from uuid import UUID, uuid4

from app.utils import aware_utcnow


class Base(SQLModel, table=True):
    uuid: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    created_at: datetime = Field(default_factory=aware_utcnow())
    updated_at: datetime = Field(
        default_factory=aware_utcnow(),
        sa_column_kwargs={"onupdate": aware_utcnow()},
    )
