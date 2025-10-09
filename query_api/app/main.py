"""Main application file for the query_api service."""

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import services, schemas

app = FastAPI()

@app.get("/items", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(services.get_db)):
    """Retrieves a list of items from the read model.

    Args:
        skip: The number of items to skip.
        limit: The maximum number of items to return.
        db: The database session.

    Returns:
        A list of items.
    """
    items = services.get_items(db, skip=skip, limit=limit)
    return items

@app.get("/items/{item_id}", response_model=schemas.Item)
def read_item(item_id: str, db: Session = Depends(services.get_db)):
    """Retrieves a single item by its ID.

    Args:
        item_id: The ID of the item to retrieve.
        db: The database session.

    Returns:
        The item with the specified ID.

    Raises:
        HTTPException: If the item is not found.
    """
    db_item = services.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item