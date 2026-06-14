import logging
import asyncio
from app.agents.base_agent import BaseOperationalAgent
from app.models.agent_model import EventPayload, AgentState
from app.services.tool_sandbox import ToolExecutionSandbox
from app.core.event_bus import LocalEventBus

logger = logging.getLogger(__name__)

class FileWriterAgent(BaseOperationalAgent):
    """
    Low-Level Action Worker.
    Listens specifically for FILE_WRITER tasks and interacts with the sandbox.
    """
    def __init__(self, agent_id: str, bus: LocalEventBus, sandbox: ToolExecutionSandbox):
        # Pass the type to the parent constructor. The base class automatically 
        # maps the async listening queue patterns under the hood.
        super().__init__(agent_id=agent_id, agent_type="FILE_WRITER", bus=bus)
        self.sandbox = sandbox

    async def execute_workflow(self, event: EventPayload):
        """Executes the physical sandbox tool sequence based on incoming event data."""
        logger.info(f"[{self.agent_id}] Activating physical file-system write sequence...")
        
        # Pull parameters from our multi-step task payload frame context
        args = event.context_data
        filename = args.get("filename", f"audit_{event.task_id}.txt")
        content = args.get("content", f"Automated execution log. Master Instruction: {event.instruction}")

        # Simulate local disk compute cycles
        await asyncio.sleep(1.0)

        # Fire the operation safely inside our traversal-protected sandbox
        result = self.sandbox.write_local_file(filename=filename, content=content)

        if not result["success"]:
            raise RuntimeError(f"Sandbox operation failed: {result.get('msg')}")
            
        logger.info(f"[{self.agent_id}] Physical operation complete. Asset stored cleanly.")
        
        # Add this to broadcast the success packet back up to the UI console window
        await self.bus.publish(
            event_type="telemetry.update",
            payload={
                "agent_id": self.agent_id,
                "agent_type": self.agent_type,
                "message": f"SUCCESS: Written compiled block asset directly to safe sandbox -> {filename}"
            }
        )