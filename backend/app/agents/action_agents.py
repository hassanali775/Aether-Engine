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
        # Register this worker to automatically listen to 'task.file_writer' topics
        super().__init__(agent_id=agent_id, agent_type="FILE_WRITER", bus=bus)
        self.sandbox = sandbox

    async def execute_workflow(self, event: EventPayload):
        """Executes the physical sandbox tool sequence based on incoming event data."""
        logger.info(f"[{self.agent_id}] Activating physical file-system write sequence...")
        
        # Pull the parameters out of our structured context dictionary
        args = event.context_data
        filename = args.get("filename", f"log_{event.task_id}.txt")
        content = args.get("content", f"Automated execution log for context: {event.instruction}")

        # Simulate local compute cycles
        await asyncio.sleep(1.0)

        # Fire the operation inside our safe sandbox container
        result = self.sandbox.write_local_file(filename=filename, content=content)

        if not result["success"]:
            raise RuntimeError(f"Sandbox operation failed: {result.get('msg')}")
            
        logger.info(f"[{self.agent_id}] Physical operation complete. Asset stored safely.")