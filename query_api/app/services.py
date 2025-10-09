
"""Services for the query_api, including database session management and queries."""

import os
from sqlalchemy.orm import Session
from shared import models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://user:password@postgres/ledger")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Gets a database session.

    Yields:
        The database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_item(db: Session, item_id: str):
    """Gets a single item by its ID.

    Args:
        db: The database session.
        item_id: The ID of the item to retrieve.

    Returns:
        The item with the specified ID, or None if not found.
    """
    return db.query(models.Item).filter(models.Item.id == item_id).first()

def get_items(db: Session, skip: int = 0, limit: int = 100):
    """Gets a list of items.

    Args:
        db: The database session.
        skip: The number of items to skip.
        limit: The maximum number of items to return.

    Returns:
        A list of items.
    """
    return db.query(models.Item).offset(skip).limit(limit).all()
