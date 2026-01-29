import time
from call_processor.engine import CallProcessor
from app_logging.manager import LogManager
from alerts.manager import AlertManager
from health.checker import HealthChecker
from circuit_breaker.registry import CircuitBreakerRegistry

def run_simulation():
    log_manager = LogManager()
    alert_manager = AlertManager()
    processor = CallProcessor(log_manager, alert_manager)
    
    # Setup Health Checker
    health_checker = HealthChecker(list(processor.services.values()))
    health_checker.start(interval=5)

    contacts = [
        {"name": "Alice"},
        {"name": "Bob"},
        {"name": "Charlie"},
        {"name": "David"},
        {"name": "Eve"}
    ]

    print("\n--- SIMULATION START: Normal Operation ---\n")
    processor.process_queue(contacts[:1]) # Process Alice

    print("\n--- SIMULATION: ElevenLabs 503 Scenario ---\n")
    # Manually trigger outage in ElevenLabs
    processor.eleven_labs.simulate_outage()
    
    # Trying to process Bob - this should trigger retries and then fail, opening the circuit
    processor.process_queue(contacts[1:2]) 

    print("\n--- SIMULATION: Circuit Breaker Open Check ---\n")
    # Trying to process Charlie while circuit is OPEN
    # Should fail fast without retries
    processor.process_queue(contacts[2:3])

    print("\n--- SIMULATION: Recovery Scenario ---\n")
    # Wait for recovery timeout or simulate recovery
    print("Simulating ElevenLabs recovery...")
    processor.eleven_labs.simulate_recovery()
    
    # Wait a bit for health checker / timeout (30s in config, let's speed it up for demo or just wait)
    # Actually, the circuit breaker allows half-open after recovery_timeout.
    # We set recovery_timeout to 30s in settings.py, let's wait long enough or modify config for demo.
    
    print("Waiting for Circuit Breaker recovery timeout (10s for demo wait)...")
    # For the sake of the demo, I'll temporarily reduce the recovery timeout or just wait.
    # I'll rely on the fact that I can force it by waiting or just continue.
    time.sleep(12) 
    # Note: I set 30s in config, 12s won't be enough if I don't change it.
    # I'll update config to 10s for the demo.
    
    print("\n--- SIMULATION: Resuming Operations ---\n")
    processor.process_queue(contacts[3:]) # Process David and Eve

    health_checker.stop()
    print("\n--- SIMULATION END ---")

if __name__ == "__main__":
    # Update settings for faster demo and to match prompt scenario
    from config import settings
    settings.SERVICE_CONFIGS["ElevenLabs"]["circuit_breaker"]["recovery_timeout"] = 10
    settings.SERVICE_CONFIGS["ElevenLabs"]["circuit_breaker"]["failure_threshold"] = 1
    
    run_simulation()
