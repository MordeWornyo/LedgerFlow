"""Main application file for the processor service."""

import asyncio
from app.services import process_commands

async def main():
    """Runs the command processing service."""
    await process_commands()

if __name__ == "__main__":
    asyncio.run(main())