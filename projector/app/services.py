"""Services for the projector, including event projection to the read model."""

import os
import json
from aiokafka import AIOKafkaConsumer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from shared.events import ItemCreatedEvent, ItemUpdatedEvent
from shared.models import Base, Item

KAFKA_BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://user:password@postgres/ledger")

engine = create_engine(DATABASE_URL)

Base.metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def _handle_item_created(event_data, db):
    """
    Handles the ItemCreatedEvent.

    Args:
        event_data: The event data.
        db: The database session.
    """
    event = ItemCreatedEvent(**event_data)
    db_item = db.query(Item).filter(Item.id == event.item_id).first()
    if not db_item:
        db_item = Item(
            id=event.item_id,
            name=event.name,
            description=event.description
        )
        db.add(db_item)
        db.commit()


def _handle_item_updated(event_data, db):
    """
    Handles the ItemUpdatedEvent.

    Args:
        event_data: The event data.
        db: The database session.
    """
    event = ItemUpdatedEvent(**event_data)
    db_item = db.query(Item).filter(Item.id == event.item_id).first()
    if db_item:
        db_item.name = event.name
        db_item.description = event.description
        db.commit()


async def project_events():
    """Consumes events from Kafka and projects them to the PostgreSQL read model."""
    consumer = AIOKafkaConsumer(
        "events",
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id="projector"
    )

    await consumer.start()

    try:
        async for msg in consumer:
            event_data = json.loads(msg.value.decode('utf-8'))
            db = SessionLocal()
            try:
                if 'name' in event_data and 'description' in event_data:
                    _handle_item_created(event_data, db)
                elif 'name' in event_data:
                    _handle_item_updated(event_data, db)
            finally:
                db.close()
    finally:
        await consumer.stop()