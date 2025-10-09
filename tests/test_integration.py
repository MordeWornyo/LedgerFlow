"""Integration tests for the LedgerFlow application."""
import os
import time
import pytest
import httpx
from kafka import KafkaProducer
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


# Service addresses for the Docker network
KAFKA_BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://user:password@postgres:5432/ledger")
COMMAND_API_URL = os.environ.get("COMMAND_API_URL", "http://command_api:8000")
QUERY_API_URL = os.environ.get("QUERY_API_URL", "http://query_api:8003")


@pytest.fixture(scope="module")
def kafka_producer():
    """Provides a Kafka producer for the test session."""
    producer = KafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    yield producer
    producer.close()


@pytest.fixture(scope="module")
def db_session():
    """Provides a database session for the test session."""
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


def test_create_item_end_to_end(kafka_producer, db_session):
    """Tests the end-to-end creation of an item.
    
    Args:
        kafka_producer: The Kafka producer fixture.
        db_session: The database session fixture.
    """
    item_name = "Test Item E2E"
    item_description = "An end-to-end test item"

    response = httpx.post(f"{COMMAND_API_URL}/items", json={
        "name": item_name,
        "description": item_description
    })
    assert response.status_code == 200

    time.sleep(5)
    item_id = None
    retries = 25

    for attempt in range(retries):
        time.sleep(2)
        resp = httpx.get(f"{QUERY_API_URL}/items")
        if resp.status_code == 200:
            items = resp.json()
            for item in items:
                if item["name"] == item_name:
                    item_id = item["id"]
                    break
        if item_id:
            print(f"Item found on attempt {attempt + 1}")
            break
        else:
            print(f"Waiting for item... attempt {attempt + 1}/{retries}")

    assert item_id is not None, (
        "Item did not appear in query_api within timeout"
    )

    with db_session.begin():
        result = db_session.execute(text("SELECT * FROM items WHERE id = :id"), {"id": item_id})
        item = result.fetchone()
        assert item is not None
        assert item.name == item_name