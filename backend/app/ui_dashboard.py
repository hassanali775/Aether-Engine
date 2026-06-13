import streamlit as st
import requests
import datetime

# ============================================================================
# COMPONENT CONFIGURATION & HIGH-DENSITY CANVAS
# ============================================================================
st.set_page_config(
    page_title="AETHER // System Mesh Matrix",
    layout="wide",
    initial_sidebar_state="collapsed"
)

BACKEND_URL = "http://127.0.0.1:8000"

# Initialize stateful UI log matrix if missing
if "mesh_traces" not in st.session_state:
    st.session_state.mesh_traces = [
        "[SYSTEM_INIT] Async local loopback routing established successfully.",
        "[FABRIC] LocalEventBus polling thread initiated inside FastAPI background event loop.",
        "[TELEMETRY] Node discovery complete. Awaiting abstract instruction sets..."
    ]

def record_trace(subsystem: str, signal: str):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
    st.session_state.mesh_traces.insert(0, f"[{timestamp}] [{subsystem.upper()}] {signal}")

# ============================================================================
# STARK INDUSTRIAL ENTERPRISE DESIGN SYSTEM (CSS INJECTION)
# ============================================================================
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #0b0e14; }
    .main { background-color: #0b0e14; color: #c9d1d9; }
    .block-container { max-width: 100%; padding: 2rem 4rem; }
    
    /* Typography: Raw Systems Engineering Spec */
    h1, h2, h3, h4 { font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace !important; font-weight: 700 !important; }
    h1 { color: #f0f6fc !important; font-size: 22px !important; letter-spacing: -0.5px; margin-bottom: 2px !important; }
    .sys-spec { color: #8b949e; font-family: monospace; font-size: 11px; letter-spacing: 1px; margin-bottom: 30px; }
    
    /* Segment Framework Bounding Blocks */
    .section-boundary { border: 1px solid #21262d; border-radius: 4px; background: #161b22; padding: 20px; margin-bottom: 20px; }
    .section-title { font-family: monospace; font-size: 12px; color: #8b949e; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 15px; padding-bottom: 6px; border-bottom: 1px solid #21262d; }
    
    /* Active Node Grid */
    .node-row { display: flex; gap: 16px; margin-bottom: 25px; }
    .node-block { flex: 1; background: #0d1117; border: 1px solid #30363d; border-radius: 4px; padding: 16px; font-family: monospace; }
    .node-id { color: #f0f6fc; font-weight: bold; font-size: 14px; }
    .node-meta { color: #8b949e; font-size: 11px; margin-top: 2px; }
    .node-status { display: inline-block; font-size: 11px; font-weight: bold; padding: 2px 6px; border-radius: 3px; margin-top: 10px; text-transform: uppercase; }
    
    /* Unified Central Control Terminal Window */
    .console-box { background: #010409; border: 1px solid #30363d; border-radius: 4px; height: 350px; overflow-y: auto; padding: 16px; font-family: "SFMono-Regular", Consolas, monospace; box-shadow: inset 0 0 15px rgba(0,0,0,0.7); }
    .console-line { color: #58a6ff; font-size: 12px; line-height: 1.6; margin: 0; padding-bottom: 4px; border-bottom: 1px solid #0d1117; }
    
    /* Command Interface Inputs & Interactive Controls */
    .stButton>button { background-color: #21262d; color: #c9d1d9; border: 1px solid #30363d; border-radius: 4px; font-family: monospace; font-size: 12px; text-transform: uppercase; letter-spacing: 1px; padding: 8px; width: 100%; transition: all 0.15s ease-in-out; }
    .stButton>button:hover { background-color: #79c0ff; color: #0b0e14; border-color: #79c0ff; }
    div.stTextArea textarea { background-color: #010409; color: #c9d1d9; border: 1px solid #30363d; border-radius: 4px; font-family: monospace; font-size: 13px; }
    div.stTextArea textarea:focus { border-color: #79c0ff; box-shadow: none; }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# RUNTIME TOPOLOGY DIAGNOSTICS DETECTOR
# ============================================================================
active_workers = []
mesh_condition = "LINK_LOST"
try:
    res = requests.get(f"{BACKEND_URL}/health", timeout=1.0)
    if res.status_code == 200:
        active_workers = res.json().get("active_workers", [])
        mesh_condition = "OPERATIONAL"
except Exception:
    pass

# ============================================================================
# SYSTEM CORE HEADER TERMINAL
# ============================================================================
st.markdown("<h1>SYSTEM_CONTROL // AETHER_ENGINE_CORE</h1>", unsafe_allow_html=True)
st.markdown(f"<div class='sys-spec'>SUBSYSTEM_STATUS: {mesh_condition} // INTERPRETER_ROUTING: ASYNC_EVENT_LOOP // DISCOVERED_THREADS: {len(active_workers)}</div>", unsafe_allow_html=True)

# ============================================================================
# MODULE VIEW 1: DISSOLVED WORKFORCE REGISTER (HORIZONTAL NODE ARCHITECTURE)
# ============================================================================
st.markdown('<div class="section-title">■ DECENTRALIZED COMPUTE NODE REGISTER</div>', unsafe_allow_html=True)

if active_workers:
    cols = st.columns(len(active_workers))
    for idx, worker in enumerate(active_workers):
        with cols[idx]:
            state = worker.get("current_state", "UNKNOWN")
            w_id = worker.get("agent_id", "NODE_ERR")
            w_type = worker.get("agent_type", "GENERIC")
            hops = worker.get("total_tasks_executed", 0)
            
            # Map clean status indicator frames based on machine state mutations
            if state == "IDLE":
                bg, text_c = "rgba(56,139,253,0.1)", "#58a6ff"
            elif state == "WORKING" or state == "COMMUNICATING":
                bg, text_c = "rgba(210,153,34,0.1)", "#d29922"
            else:
                bg, text_c = "rgba(248,81,73,0.1)", "#f85149"
                
            st.markdown(f"""
                <div class="node-block">
                    <div class="node-id">{w_id}</div>
                    <div class="node-meta">CLASS: {w_type}</div>
                    <div class="node-meta">PROCESSED_HOPS: {hops}</div>
                    <div class="node-status" style="background: {bg}; color: {text_c}; border: 1px solid {text_c}33;">[{state}]</div>
                </div>
            """, unsafe_allow_html=True)
else:
    st.markdown(
        "<div style='background:#0d1117; border:1px dashed #f85149; border-radius:4px; padding:20px; font-family:monospace; font-size:12px; color:#f85149; text-align:center;'>"
        "CRITICAL ERROR: Telemetry broker pipeline offline. Ensure local ASGI Uvicorn app server is active on port 8000."
        "</div>",
        unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================================
# MODULE VIEW 2: HIGH-DENSITY FLOW CONTROL WORKSPACE
# ============================================================================
st.markdown('<div class="section-title">■ DISPATCH BOUNDARY & DATA ROUTING CHANNELS</div>', unsafe_allow_html=True)

# One main structural row to prevent copying the look of previous layouts
col_left, col_right = st.columns([1, 1.5])

with col_left:
    st.markdown('<div class="section-boundary" style="margin-bottom:0px; height:350px;">', unsafe_allow_html=True)
    st.markdown("<div style='font-family:monospace; font-size:12px; color:#8b949e; margin-bottom:10px;'>RAW INST_BUFFER_ARRAY:</div>", unsafe_allow_html=True)
    
    instruction_buffer = st.text_area(
        "inst_buffer", 
        label_visibility="collapsed",
        placeholder="Input raw execution commands to decompose into the broker mesh...",
        height=190
    )
    
    st.markdown("<div style='margin-top:15px;'></div>", unsafe_allow_html=True)
    
    if st.button("Publish Frame to Bus"):
        if instruction_buffer.strip():
            try:
                record_trace("gateway", f"Intercepted target array -> Transmitting to central Orchestrator event topic.")
                response = requests.post(f"{BACKEND_URL}/api/orchestrate", params={"instruction": instruction_buffer})
                
                if response.status_code == 200:
                    allocated_trace = response.json().get("assigned_task_id")
                    record_trace("event_bus", f"SUCCESS: Enqueued payload frame. Core trace hash assigned: {allocated_trace}")
                else:
                    record_trace("gateway_fault", f"REJECT: Edge routing configuration refused data frames. Code {response.status_code}")
            except Exception as e:
                record_trace("sys_error", f"EXCEPTION: Asynchronous transport layer drop -> {str(e)}")
        else:
            st.error("Execution payload buffer cannot evaluate to null.")
            
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    # Aggregated Live Log Feed Output Frame
    log_stream_html = "".join([f'<p class="console-box console-line">{log}</p>' for log in st.session_state.mesh_traces])
    st.markdown(f'<div class="console-box">{log_stream_html}</div>', unsafe_allow_html=True)

# ============================================================================
# INTERFACE CONTROLS & TRACE RE-SYNC INDEX
# ============================================================================
st.markdown("<br>", unsafe_allow_html=True)
foot_l, foot_r = st.columns([1, 6])
with foot_l:
    if st.button("Flush Console Traces"):
        st.session_state.mesh_traces = [f"[{datetime.datetime.now().strftime('%H:%M:%S')}] [UI] Operational telemetry logs cleared cleanly."]
        st.rerun()