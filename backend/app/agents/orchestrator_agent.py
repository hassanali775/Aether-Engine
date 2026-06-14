import logging
import asyncio
from app.models.agent_model import EventPayload, AgentState
from app.services.llm_service import LocalLLMService
from app.core.event_bus import LocalEventBus
from app.agents.base_agent import BaseOperationalAgent

logger = logging.getLogger(__name__)

class OrchestratorAgent(BaseOperationalAgent):
    """
    High-Tier Mesh Coordinator.
    Compiles abstract objectives into multi-step execution plans and manages the sequence loop.
    """
    def __init__(self, agent_id: str, bus: LocalEventBus, llm_service: LocalLLMService):
        super().__init__(agent_id=agent_id, agent_type="ORCHESTRATOR", bus=bus)
        self.llm = llm_service
        self.execution_history = []
        
        self.declared_tools = [
            {"name": "FILE_WRITER", "description": "Writes text data, system status, or logs to disk. Args: {'filename': 'str', 'content': 'str'}"},
            {"name": "SYSTEM_DIAGNOSTIC", "description": "Generates a simulated system metric health payload. Args: {'scope': 'str'}"}
        ]

    async def execute_workflow(self, event: EventPayload):
        print(f"\n[ORCHESTRATOR TRACE] Intercepted payload for task: {event.task_id}")
        print(f"[ORCHESTRATOR TRACE] Processing instruction loop: '{event.instruction}'")
        self.current_state = AgentState.COMMUNICATING
        
        task_pipeline = await self.llm.decompose_instruction(
            raw_instruction=event.instruction,
            available_tools=self.declared_tools
        )
        
        print(f"[ORCHESTRATOR TRACE] Sub-task sequence compiled! Active actions to process: {len(task_pipeline)}")
        self.current_state = AgentState.WORKING
        
        for task in task_pipeline:
            tool = task.get("tool_to_use", "FILE_WRITER")
            args = task.get("args", {})
            step = task.get("step_sequence", 1)
            
            # Formulate the target channel key to exactly match base_agent subscribe logic
            target_topic = f"task.{tool.lower().strip()}"
            print(f"[ORCHESTRATOR TRACE] Publishing Step {step} down-stream to channel: {target_topic}")
            
            self.execution_history.append({"step": step, "tool": tool, "status": "DISPATCHED"})
            
            await self.bus.publish(
                event_type=target_topic,
                payload={
                    "task_id": f"sub_{step}_{event.task_id}",
                    "sender_id": self.agent_id,
                    "target_agent_type": tool,
                    "instruction": f"Execute step {step} compiled instructions.",
                    "context_data": args
                }
            )
            await asyncio.sleep(0.2)
            
        print(f"[{self.agent_id}] Sequential delegation loop completed successfully.")