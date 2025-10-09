"""Command models for the LedgerFlow application."""

from pydantic import BaseModel

class CreateItemCommand(BaseModel):
    """Command to create a new item.

    Attributes:
        name: The name of the item.
        description: A description of the item.
    """
    name: str
    description: str | None = None

class UpdateItemCommand(BaseModel):
    """Command to update an existing item.

    Attributes:
        item_id: The unique identifier for the item to update.
        name: The new name of the item.
        description: The new description of the item.
    """
    item_id: str
    name: str
    description: str | None = None