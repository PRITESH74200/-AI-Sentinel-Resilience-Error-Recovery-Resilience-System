import streamlit as st
import time
import json
import pandas as pd
from datetime import datetime
from call_processor.engine import CallProcessor
from app_logging.manager import LogManager
from alerts.manager import AlertManager
from config import settings

# Customizing Streamlit Page
st.set_page_config(page_title="AI Sentinel Resilience Dashboard", layout="wide")

st.title("🛡️ AI Sentinel: Error Recovery Dashboard")
st.markdown("""
This dashboard simulates the **AI Call Agent's resilience system**. 
You can trigger failures, monitor circuit breaker states, and observe exponential backoff in real-time.
""")

# Sidebar settings
st.sidebar.header("System Configuration")
eleven_timeout = st.sidebar.slider("ElevenLabs Recovery Timeout (s)", 5, 60, 10)
eleven_threshold = st.sidebar.number_input("ElevenLabs Failure Threshold", 1, 5, 1)

# Update settings based on UI
settings.SERVICE_CONFIGS["ElevenLabs"]["circuit_breaker"]["recovery_timeout"] = eleven_timeout
settings.SERVICE_CONFIGS["ElevenLabs"]["circuit_breaker"]["failure_threshold"] = eleven_threshold

# Initialize components
if 'log_data' not in st.session_state:
    st.session_state.log_data = []

class StreamlitLogManager(LogManager):
    def info(self, message: str):
        super().info(message)
        st.session_state.log_data.append({"Time": datetime.now().strftime("%H:%M:%S"), "Level": "INFO", "Message": message})

    def error(self, service_name: str, category: str, message: str, retry_count: int = 0, state: str = "N/A"):
        super().error(service_name, category, message, retry_count, state)
        st.session_state.log_data.append({
            "Time": datetime.now().strftime("%H:%M:%S"), 
            "Level": "ERROR", 
            "Message": f"[{service_name}] {message} (Retry: {retry_count})"
        })

# Scenario Control
col1, col2 = st.columns(2)

with col1:
    st.subheader("Control Center")
    sim_type = st.radio("Select Scenario", ["Normal Operation", "ElevenLabs 503 Failure"])
    run_btn = st.button("Run Simulation Step")

with col2:
    st.subheader("System Status")
    # This is a bit tricky since we don't have a persistent state across clicks easily for the processor
    # But we can simulate the state.
    if 'eleven_healthy' not in st.session_state:
        st.session_state.eleven_healthy = True
    
    status_color = "green" if st.session_state.eleven_healthy else "red"
    st.markdown(f"**ElevenLabs Service Status:** :{status_color}[{'HEALTHY' if st.session_state.eleven_healthy else 'DOWN (503)'}]")

if run_btn:
    log_manager = StreamlitLogManager()
    alert_manager = AlertManager()
    processor = CallProcessor(log_manager, alert_manager)
    
    if sim_type == "ElevenLabs 503 Failure":
        processor.eleven_labs.simulate_outage()
        st.session_state.eleven_healthy = False
    else:
        processor.eleven_labs.simulate_recovery()
        st.session_state.eleven_healthy = True

    with st.spinner("Processing call..."):
        processor.process_queue([{"name": "Dynamic User"}])
    
    st.success("Simulation step completed.")

# Display Logs
st.subheader("Real-time Event Logs")
if st.session_state.log_data:
    df = pd.DataFrame(st.session_state.log_data[::-1]) # Show latest first
    st.table(df)
else:
    st.info("No logs generated yet. Run a simulation step.")

# Display Architecture
with st.expander("View System Architecture"):
    st.image("https://raw.githubusercontent.com/PRITESH74200/-AI-Sentinel-Resilience-Error-Recovery-Resilience-System/main/evidence/architecture_diagram.txt", caption="Architecture Flow")
    st.code("""
    - Exponential Backoff (5s, 10s, 20s)
    - Circuit Breaker (Trips on failure)
    - Fail-fast (Skips calls when down)
    - Automatic Recovery (Half-Open states)
    """)
