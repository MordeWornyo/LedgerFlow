
"""Main application file for the command_api service."""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from aiokafka import AIOKafkaProducer
from shared.commands import CreateItemCommand
from .services import get_kafka_producer, send_command, close_kafka_producer

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manages the application's lifespan."""
    await get_kafka_producer()
    yield
    await close_kafka_producer()

app = FastAPI(lifespan=lifespan)

@app.post("/items")
async def create_item(
    command: CreateItemCommand, producer: AIOKafkaProducer = Depends(get_kafka_producer)
):
    """Handles the creation of a new item by sending a command to Kafka.

    Args:
        command: The command to create a new item.
        producer: The Kafka producer instance.

    Returns:
        A dictionary with the status of the operation.
    """
    await send_command(command, producer)
    return {"status": "ok"}
