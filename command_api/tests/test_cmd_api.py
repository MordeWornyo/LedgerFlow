"""Tests for the Command API."""
import pytest
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient
from command_api.app.main import app
from command_api.app.services import get_kafka_producer


@pytest.fixture
def client():
    """Provides a test client for the application."""
    return TestClient(app)


@pytest.mark.asyncio
async def test_create_item(client):
    """Tests the creation of an item.

    Args:
        client: The test client.
    """
    mock_producer = AsyncMock()
    mock_producer.send_and_wait = AsyncMock()

    async def override_get_kafka_producer():
        """Overrides the Kafka producer dependency for testing."""
        return mock_producer

    # Override the dependency
    app.dependency_overrides[get_kafka_producer] = override_get_kafka_producer

    response = client.post(
        "/items", json={"name": "Test Item", "description": "A test item"}
    )

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    mock_producer.send_and_wait.assert_called_once()

    # Clear overrides after the test
    app.dependency_overrides.clear()
