"""Database models for the LedgerFlow application."""

from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Item(Base):
    """Represents an item in the read model.

    Attributes:
        id: The unique identifier for the item.
        name: The name of the item.
        description: A description of the item.
    """
    __tablename__ = "items"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)