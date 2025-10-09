"""Tests for the Query API."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from unittest.mock import MagicMock
from query_api.app.main import app
from query_api.app.services import get_db
from shared.models import Item


@pytest.fixture
def client():
    """Provides a test client for the application."""
    return TestClient(app)


@pytest.fixture
def db_session():
    """Provides a mock database session for testing."""
    return MagicMock(spec=Session)


@pytest.mark.asyncio
async def test_read_items(client, db_session):
    """Tests reading all items.

    Args:
        client: The test client.
        db_session: The mock database session.
    """
    test_item = Item(id="test-id", name="Test Item", description="A test item")

    db_session.query.return_value.offset.return_value.limit.return_value.all.return_value = (
        [test_item]
    )

    # dependency override
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    response = client.get("/items")

    assert response.status_code == 200
    assert response.json() == [
        {"id": "test-id", "name": "Test Item", "description": "A test item"}
    ]

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_read_item(client, db_session):
    """Tests reading a single item.

    Args:
        client: The test client.
        db_session: The mock database session.
    """
    test_item = Item(id="test-id", name="Test Item", description="A test item")

    db_session.query.return_value.filter.return_value.first.return_value = test_item

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    response = client.get("/items/test-id")

    assert response.status_code == 200
    assert response.json() == {
        "id": "test-id",
        "name": "Test Item",
        "description": "A test item",
    }

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_read_item_not_found(client, db_session):
    """Tests reading a non-existent item.

    Args:
        client: The test client.
        db_session: The mock database session.
    """
    db_session.query.return_value.filter.return_value.first.return_value = None

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    response = client.get("/items/non-existent-id")

    assert response.status_code == 404

    app.dependency_overrides.clear()