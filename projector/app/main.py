"""Main application file for the projector service."""

import asyncio
from .services import project_events

async def main():
    """Runs the event projection service."""
    await project_events()

if __name__ == "__main__":
    asyncio.run(main())