import asyncio
import logging
from typing import Dict, Any
from app.core.event_bus import LocalEventBus
from app.models.agent_model import AgentState, AgentTelemetry, EventPayload

logger = logging.getLogger(__name__)

class BaseOperationalAgent:
    """
    Polymorphic Edge Agent Core.
    Maintains an independent background event listener loop and autonomous state mutations.
    """
    def __init__(self, agent_id: str, agent_type: str, bus: LocalEventBus):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.bus = bus
        
        # Internal state tracking
        self.current_state = AgentState.IDLE
        self.total_tasks_executed = 0
        self.current_task_id = None

        # Automatically register this agent's listener loop to its matching profile topic
        self.bus.subscribe(event_type=f"task.{self.agent_type.lower()}", callback=self.handle_incoming_event)

    def get_telemetry(self) -> AgentTelemetry:
        """Surfaces the active running metrics of this isolated worker instance."""
        return AgentTelemetry(
            agent_id=self.agent_id,
            agent_type=self.agent_type,
            current_state=self.current_state,
            total_tasks_executed=self.total_tasks_executed,
            current_task_id=self.current_task_id
        )

    async def handle_incoming_event(self, payload: Dict[str, Any]):
        """Callback loop interceptor. Converts raw payloads into domain models and triggers execution."""
        try:
            event = EventPayload(**payload)
            
            # Ignore tasks this agent generated to avoid endless echo loops
            if event.sender_id == self.agent_id:
                return

            logger.info(f"[{self.agent_id}] Intercepted job routing trace: {event.task_id}")
            
            # Transition state machine to active processing
            self.current_state = AgentState.WORKING
            self.current_task_id = event.task_id

            # Execute the abstract processing routine overridden by downstream worker scripts
            await self.execute_workflow(event)

            # Task tracking updates
            self.total_tasks_executed += 1
            self.current_state = AgentState.IDLE
            self.current_task_id = None
            
            # Broadcast metrics update across the event fabric
            await self.bus.publish(
                event_type="telemetry.update", 
                payload=self.get_telemetry().model_dump()
            )

        except Exception as e:
            self.current_state = AgentState.FAULTED
            logger.error(f"[{self.agent_id} CRITICAL RUNTIME CRASH] Failure executing task: {str(e)}")
            await self.bus.publish(
                event_type="telemetry.fault",
                payload={"agent_id": self.agent_id, "task_id": self.current_task_id, "error": str(e)}
            )

    async def execute_workflow(self, event: EventPayload):
        """
        Abstract execution boundary. 
        Must be overridden by inheriting agent instances to fulfill custom domain goals.
        """
        raise NotImplementedError("Downstream inheriting sub-agents must declare custom workflow loops.")