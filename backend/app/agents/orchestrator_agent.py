import logging
from app.agents.base_agent import BaseOperationalAgent
from app.models.agent_model import EventPayload, AgentState
from app.services.llm_service import LocalLLMService
from app.core.event_bus import LocalEventBus

logger = logging.getLogger(__name__)

class OrchestratorAgent(BaseOperationalAgent):
    """
    High-Tier Mesh Coordinator.
    Intercepts raw input strings, uses local SLM intelligence to map tools,
    and publishes structured tasks back into the event loop.
    """
    def __init__(self, agent_id: str, bus: LocalEventBus, llm_service: LocalLLMService):
        super().__init__(agent_id=agent_id, agent_type="ORCHESTRATOR", bus=bus)
        self.llm = llm_service
        
        # Define the structural boundaries of what your engine can do
        self.declared_tools = [
            {"name": "FILE_WRITER", "description": "Writes text or data logs cleanly to the local file system storage."},
            {"name": "SYSTEM_DIAGNOSTIC", "description": "Compiles runtime health traces and scans CPU metrics."}
        ]

    async def execute_workflow(self, event: EventPayload):
        """Processes the workflow loop by executing local SLM text-to-tool compilation."""
        logger.info(f"[{self.agent_id}] Decomposing payload task tree via local inference engine...")
        
        # Update state matrix to communicating during model generation call
        self.current_state = AgentState.COMMUNICATING
        
        parsed_action = await self.llm.decompose_instruction(
            raw_instruction=event.instruction,
            available_tools=self.declared_tools
        )
        
        logger.info(f"[{self.agent_id}] SLM Inference Completed. Mapped Action: {parsed_action.get('tool_to_use')}")
        
        # Route the resulting action back onto the event bus as a fresh task for downstream workers
        target_topic = f"task.{parsed_action.get('tool_to_use', 'fallback').lower()}"
        payload_to_broadcast = {
            "task_id": f"sub_{event.task_id}",
            "sender_id": self.agent_id,
            "target_agent_type": parsed_action.get("tool_to_use"),
            "instruction": f"Execute action mapped from instruction: {event.instruction}",
            "context_data": parsed_action.get("args", {})
        }
        
        await self.bus.publish(event_type=target_topic, payload=payload_to_broadcast)