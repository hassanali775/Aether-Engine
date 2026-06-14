import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.event_bus import LocalEventBus
from app.services.llm_service import LocalLLMService
from app.services.tool_sandbox import ToolExecutionSandbox
from app.agents.orchestrator_agent import OrchestratorAgent
from app.agents.action_agents import FileWriterAgent

# 1. Initialize core in-memory platform modules
event_bus = LocalEventBus()
llm_engine = LocalLLMService()
sandbox = ToolExecutionSandbox()
active_agents: dict = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles async background task loops upon server startup and shutdown."""
    print("\n[SYSTEM BOOT] Starting Central Message Broker Processing Loop...")
    bus_task = asyncio.create_task(event_bus.start_processing_loop())
    
    # Instantiate the Orchestrator
    print("[SYSTEM BOOT] Mounting Orchestrator Prime Node...")
    orchestrator = OrchestratorAgent(
        agent_id="orchestrator_prime", 
        bus=event_bus, 
        llm_service=llm_engine
    )
    active_agents[orchestrator.agent_id] = orchestrator

    # Instantiate the FileWriterAgent
    print("[SYSTEM BOOT] Mounting File Writer Worker Node...")
    file_worker = FileWriterAgent(
        agent_id="worker_file_01", 
        bus=event_bus, 
        sandbox=sandbox
    )
    active_agents[file_worker.agent_id] = file_worker
    
    yield
    
    # Graceful shutdown sequence
    print("[SYSTEM SHUTDOWN] Stopping processing loops cleanly...")
    event_bus.stop_processing_loop()
    bus_task.cancel()
app = FastAPI(title="Aether Engine Core Backend", lifespan=lifespan)

@app.get("/health")
async def health_check():
    return {
        "status": "online", 
        "engine": "Aether Multi-Agent Mesh",
        "active_workers": [agent.get_telemetry() for agent in active_agents.values()]
    }

@app.post("/api/orchestrate")
async def process_user_objective(instruction: str):
    """Drops abstract commands directly into the decentralized routing fabric."""
    task_id = f"task_root_{int(asyncio.get_event_loop().time())}"
    
    payload = {
        "task_id": task_id,
        "sender_id": "api_gateway",
        "target_agent_type": "ORCHESTRATOR",
        "instruction": instruction,
        "context_data": {}
    }
    
    # Must be lowercase to match the BaseOperationalAgent setup
    await event_bus.publish(event_type="task.orchestrator", payload=payload)
    return {"status": "objective_received", "assigned_task_id": task_id}