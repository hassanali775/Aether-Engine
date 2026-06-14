# Distributed Multi-Agent Task Orchestration Engine

A decoupled, event-driven task orchestration runtime designed to compile natural language objectives into secure tool execution paths. The system utilizes an in-memory asynchronous message broker fabric to delegate tasks across independent worker nodes, implementing strict schema validation policies and path-traversal guarded sandbox environments for fault-tolerant operation.

## Architectural Overview

Unlike traditional monolithic LLM frameworks that execute actions synchronously, this engine decouples the task ingestion gateway from the execution environment. The architecture is modeled after enterprise micro-agent topologies:

1. **Ingestion Gateway:** Intercepts raw string payloads and forwards instructions to the backend routing pool.
2. **Orchestrator Core:** Compiles the sub-task execution graph and schedules action sequences.
3. **Policy Validator:** Enforces Small Language Model (SLM) structural schema integrity checks before downstream dispatching.
4. **Adaptive Recovery Layer:** Catches structural mismatches or LLM core anomalies, automatically engaging a safe-path tool map fallback to dynamically parse operational parameters (such as scopes and target boundaries) without dropping execution state.
5. **Worker Nodes:** Decoupled processes that intercept broker queues to execute operations inside sandboxed file-system layers.

---

## Technical Stack & Infrastructure

* **Backend Engine:** FastAPI, Uvicorn (Non-blocking Asyncio event loop)
* **Orchestration Topology:** In-memory decoupled broker channels (`task.orchestrator`, `task.file_writer`)
* **Control Plane Dashboard:** Streamlit micro-frontend with real-time telemetry streaming
* **Security Context:** Path-traversal guarding, sandbox profile isolation

---

## Core System Mechanics

### Real-Time Telemetry and Tracing

The platform streams execution traces across the entire life cycle of a transaction. When an LLM compilation variance occurs, the telemetry state captures the recovery sequence seamlessly:

```log
[GATEWAY] Intercepted raw string payload.
[GATEWAY] Forwarding objective instruction to backend routing pool...
[ORCHESTRATOR] Intercepted incoming payload frame: task_root_5848
[ROUTING_POLICIES] SLM structural schema mismatch caught by policy validator.
[ROUTING_POLICIES] Fallback policy engaged: Successfully resolved sequence to safe-path tool map.
[ORCHESTRATOR] Task compilation completed. Active jobs in graph: 1
[ORCHESTRATOR] Dispatching Step 1 down-stream to channel: task.file_writer
[WORKER_NODE] FileWriterAgent intercepted task context from broker queue.
[WORKER_NODE] Invoking path-traversal guarded sandbox tools...
[WORKER_NODE] File-system write verified. State transaction complete.