
"""Services for the command_api, including Kafka producer management."""

import os
from aiokafka import AIOKafkaProducer
from shared.commands import CreateItemCommand

KAFKA_BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")

producer: AIOKafkaProducer | None = None

async def get_kafka_producer() -> AIOKafkaProducer:
    """Gets a singleton instance of the Kafka producer.

    Returns:
        The Kafka producer instance.
    """
    global producer
    if producer is None:
        producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
        await producer.start()
    return producer

async def close_kafka_producer():
    """Closes the Kafka producer instance."""
    global producer
    if producer:
        await producer.stop()
        producer = None

async def send_command(command: CreateItemCommand, producer: AIOKafkaProducer):
    """Sends a command to the 'commands' Kafka topic.

    Args:
        command: The command to send.
        producer: The Kafka producer instance to use.
    """
    await producer.send_and_wait("commands", command.json().encode("utf-8"))
