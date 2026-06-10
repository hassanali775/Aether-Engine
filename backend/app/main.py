import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.event_bus import LocalEventBus

# Initialize the global event bus instance
event_bus = LocalEventBus()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles async background task loops upon server startup and shutdown."""
    # Run the event bus consumption queue inside the asyncio event loop background
    bus_task = asyncio.create_task(event_bus.start_processing_loop())
    yield
    # Gracefully wind down on shutdown
    event_bus.stop_processing_loop()
    bus_task.cancel()

app = FastAPI(title="Aether Engine Core Backend", lifespan=lifespan)

@app.get("/health")
async def health_check():
    return {"status": "online", "engine": "Aether Multi-Agent Mesh"}