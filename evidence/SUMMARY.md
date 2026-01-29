# Evidence Summary - AI Call Agent Resilience

This folder contains evidence of the system's successful implementation and operation as per the project requirements.

## Files Included:
- **[architecture_diagram.txt](architecture_diagram.txt)**: A text-based representation of the system design and component interactions.
- **[simulation_output.txt](simulation_output.txt)**: Direct terminal output from `main.py`, demonstrating the successful handling of the ElevenLabs 503 scenario, including:
    - Initial success.
    - Transient error detection & retry logic.
    - Circuit breaker state transition to OPEN.
    - Fail-fast operation during the outage.
    - Health check detection and successful recovery.
- **[app_errors_snapshot.txt](app_errors_snapshot.txt)**: A snapshot of the structured JSON logs generated during the simulation, showing detailed error categories and service states.

## Key Observations:
1. **Scenario 1 (Normal)**: Alice's call completed without issues.
2. **Scenario 2 (Outage)**: Bob's call triggered 3 retries (5s, 10s, 20s exponential backoff) before tripping the ElevenLabs circuit.
3. **Scenario 3 (Fail-Fast)**: Charlie's call was immediately skipped because the circuit was OPEN, preventing unnecessary resource consumption.
4. **Scenario 4 (Recovery)**: After a 10s timeout and positive health check, the circuit reset, and calls for David and Eve succeeded.
