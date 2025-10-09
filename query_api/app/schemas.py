"""Pydantic schemas for the query_api."""

from pydantic import BaseModel

class Item(BaseModel):
    """Schema for an item in the read model.

    Attributes:
        id: The unique identifier for the item.
        name: The name of the item.
        description: A description of the item.
    """
    id: str
    name: str
    description: str | None = None

    class Config:
        """Pydantic configuration.

        Attributes:
            orm_mode: Whether to allow ORM mode.
        """
        orm_mode = True