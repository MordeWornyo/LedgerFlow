"""Event models for the LedgerFlow application."""

from pydantic import BaseModel

class ItemCreatedEvent(BaseModel):
    """Event indicating that a new item has been created.

    Attributes:
        item_id: The unique identifier for the item.
        name: The name of the item.
        description: A description of the item.
    """
    item_id: str
    name: str
    description: str | None = None

class ItemUpdatedEvent(BaseModel):
    """Event indicating that an existing item has been updated.

    Attributes:
        item_id: The unique identifier for the item that was updated.
        name: The new name of the item.
        description: The new description of the item.
    """
    item_id: str
    name: str
    description: str | None = None