import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.event_bus import LocalEventBus
from app.services.llm_service import LocalLLMService
from app.agents.orchestrator_agent import OrchestratorAgent

# 1. Instantiate the asynchronous core platform systems
event_bus = LocalEventBus()
llm_engine = LocalLLMService()
active_agents: dict = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles async background task loops upon server startup and shutdown."""
    # Start the central message broker background polling routine
    bus_task = asyncio.create_task(event_bus.start_processing_loop())
    
    # Instantiate your intelligent Orchestrator Agent layer
    orchestrator = OrchestratorAgent(
        agent_id="orchestrator_prime", 
        bus=event_bus, 
        llm_service=llm_engine
    )
    active_agents[orchestrator.agent_id] = orchestrator
    
    yield
    # Gracefully spin down on shutdown
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
    """Production Endpoint. Drops abstract commands straight into the intelligent routing fabric."""
    task_id = f"task_root_{int(asyncio.get_event_loop().time())}"
    
    payload = {
        "task_id": task_id,
        "sender_id": "api_gateway",
        "target_agent_type": "ORCHESTRATOR",
        "instruction": instruction,
        "context_data": {}
    }
    
    # Broadcast to the orchestrator queue
    await event_bus.publish(event_type="task.orchestrator", payload=payload)
    return {"status": "objective_received", "assigned_task_id": task_id}