from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from enum import Enum

class AgentState(str, Enum):
    IDLE = "IDLE"
    WORKING = "WORKING"
    COMMUNICATING = "COMMUNICATING"
    FAULTED = "FAULTED"

class AgentTelemetry(BaseModel):
    agent_id: str
    agent_type: str
    current_state: AgentState
    total_tasks_executed: int = 0
    current_task_id: Optional[str] = None

class EventPayload(BaseModel):
    task_id: str
    sender_id: str
    target_agent_type: str
    instruction: str
    context_data: Dict[str, Any] = Field(default_factory=dict)