import pytest
from unittest.mock import AsyncMock
from command_api.app import services
from shared.commands import CreateItemCommand


@pytest.mark.asyncio
async def test_get_kafka_producer_starts_once(monkeypatch):
    """Tests that the producer is created only once and cached."""
    mock_producer = AsyncMock()
    mock_start = AsyncMock()
    monkeypatch.setattr(services, "AIOKafkaProducer", lambda **_: mock_producer)
    mock_producer.start = mock_start

    first = await services.get_kafka_producer()
    second = await services.get_kafka_producer()

    assert first is second
    mock_start.assert_called_once()


@pytest.mark.asyncio
async def test_close_kafka_producer_stops_and_resets(monkeypatch):
    """Tests that the producer is closed correctly and reset to None."""
    mock_producer = AsyncMock()
    services.producer = mock_producer

    await services.close_kafka_producer()

    mock_producer.stop.assert_awaited_once()
    assert services.producer is None


@pytest.mark.asyncio
async def test_send_command_calls_producer_send_and_wait():
    """Tests that the command is serialized and sent to Kafka."""
    mock_producer = AsyncMock()
    command = CreateItemCommand(name="test", description="desc")

    await services.send_command(command, mock_producer)

    mock_producer.send_and_wait.assert_called_once_with(
        "commands", command.json().encode("utf-8")
    )