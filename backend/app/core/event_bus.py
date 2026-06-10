import asyncio
from typing import Dict, Any, Callable, List
import logging

logger = logging.getLogger(__name__)

class LocalEventBus:
    """
    In-Memory Asynchronous Message Broker.
    Orchestrates decoupled, non-blocking agent-to-agent telemetry and task routing.
    """
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}
        self._queue: asyncio.Queue = asyncio.Queue()
        self._running = False

    def subscribe(self, event_type: str, callback: Callable):
        """Registers an agent loop callback listener to a specific event topic."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)

    async def publish(self, event_type: str, payload: Dict[str, Any]):
        """Enqueues an event payload into the asynchronous processing loop."""
        event = {"type": event_type, "payload": payload}
        await self._queue.put(event)

    async def start_processing_loop(self):
        """Starts the infinite background polling consumption broker loop."""
        self._running = True
        logger.info("[EVENT BUS] Initializing core asynchronous message routing...")
        while self._running:
            try:
                event = await self._queue.get()
                event_type = event["type"]
                payload = event["payload"]

                if event_type in self._subscribers:
                    tasks = [callback(payload) for callback in self._subscribers[event_type]]
                    await asyncio.gather(*tasks, return_exceptions=True)

                self._queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"[EVENT BUS CRITICAL FAULT] Routing execution failure: {str(e)}")

    def stop_processing_loop(self):
        """Gracefully halts the event bus consumption layers."""
        self._running = False