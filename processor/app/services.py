"""Services for the processor, including command processing."""

import os
import json
import uuid
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from shared.commands import CreateItemCommand, UpdateItemCommand
from shared.events import ItemCreatedEvent, ItemUpdatedEvent

KAFKA_BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")


async def _handle_create_item(command_data, producer):
    """
    Handles the CreateItemCommand.

    Args:
        command_data: The command data.
        producer: The Kafka producer.
    """
    command = CreateItemCommand(**command_data)
    item_id = uuid.uuid4().hex
    event = ItemCreatedEvent(
        item_id=item_id,
        name=command.name,
        description=command.description
    )
    await producer.send_and_wait("events", event.json().encode("utf-8"))


async def _handle_update_item(command_data, producer):
    """
    Handles the UpdateItemCommand.

    Args:
        command_data: The command data.
        producer: The Kafka producer.
    """
    command = UpdateItemCommand(**command_data)
    event = ItemUpdatedEvent(
        item_id=command.item_id,
        name=command.name,
        description=command.description
    )
    await producer.send_and_wait("events", event.json().encode("utf-8"))


async def process_commands():
    """Consumes commands from Kafka, processes them, and produces events."""
    consumer = AIOKafkaConsumer(
        "commands",
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id="processor"
    )
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)

    await consumer.start()
    await producer.start()

    try:
        async for msg in consumer:
            command_data = json.loads(msg.value.decode('utf-8'))

            if 'item_id' in command_data:
                await _handle_update_item(command_data, producer)
            else:
                await _handle_create_item(command_data, producer)
    finally:
        await consumer.stop()
        await producer.stop()