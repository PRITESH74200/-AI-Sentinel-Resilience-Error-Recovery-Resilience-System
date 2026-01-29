# AI Call Agent - Error Recovery & Resilience System

## Architecture Overview
This system is designed to handle failures in a distributed AI architecture where multiple third-party services are consumed. It follows a modular design with clear separation of concerns between error detection, recovery strategies, and observability.

### Core Components
- **Config-Driven**: All retry and circuit breaker parameters are centralized in `config/settings.py`.
- **Exception Hierarchy**: Differentiates between `TransientError` (retryable) and `PermanentError` (fatal).
- **Retry Strategy**: Implements exponential backoff with jitter to prevent cascading failures.
- **Circuit Breaker**: Implements a per-service state machine (CLOSED, OPEN, HALF-OPEN) to protect downstream services and fail fast.
- **Observability**: Multi-channel logging (local structured JSON + Google Sheets abstraction) and alerting (Email, Telegram, Webhook).
- **Health System**: Background checks to monitor service availability and facilitate recovery.

## Error Flow
1. **Detection**: Service wrappers catch raw exceptions and map them to the custom hierarchy.
2. **Evaluation**: The `CallProcessor` uses `RetryStrategy` for `TransientErrors`.
3. **Execution**: If retries fail or a threshold is met, the `CircuitBreaker` trips to `OPEN`.
4. **Alerting**: Critical failures and state transitions trigger the `AlertManager`.
5. **Recovery**: The `HealthChecker` monitors services. Once healthy and the timeout period passes, the breaker transitions to `HALF_OPEN` to test the waters, then back to `CLOSED`.

## Resilience Logic
- **Exponential Backoff**: `delay = initial_delay * (base ** attempt) + jitter`.
- **Fail-Fast**: Once the circuit is `OPEN`, subsequent calls return instantly to avoid hanging resources.
- **Graceful Degradation**: If a service fails permanently for a specific contact, the system logs the failure, alerts the admin, and moves to the next contact in the queue without crashing.

## Scenario: ElevenLabs 503
1. **Detection**: `ElevenLabsService` raises `ServiceUnavailableError`.
2. **Retry**: `RetryStrategy` attempts 3 retries with 5s, 10s, 20s delays (plus jitter).
3. **Failure**: After 3 attempts fail, the error is logged and an alert is sent.
4. **Circuit Trip**: The failure count reaches the threshold (3), and the `CircuitBreaker` for `ElevenLabs` opens.
5. **Next Step**: The system skips the current call and proceeds to the next contact.
6. **Recovery**: Once `ElevenLabs` is simulated as healthy, the breaker resets on the next successful call after the timeout.

## Implementation Details
- **No external resilience libraries**: Built from scratch using Python standard features.
- **Thread-safe Health Checker**: Runs in a background daemon thread.
- **Structured Logs**: JSON format for easy ingestion by log aggregators.
- **Mocks**: `ElevenLabs`, `LLM`, and `CRM` are mocked to demonstrate failure scenarios.

## Running the Simulation
Execute the main script:
```bash
python main.py
```
This will run through a sequence of normal operation, outage simulation, fail-fast behavior, and recovery.

## Evidence & Verification
Detailed execution logs, architecture diagrams, and simulation summaries can be found in the [evidence/](evidence/) folder.
- [Simulation Output](evidence/simulation_output.txt)
- [Log Snapshot](evidence/app_errors_snapshot.log)
- [Architecture Diagram](evidence/architecture_diagram.txt)
- [Evidence Summary](evidence/SUMMARY.md)

## Example Logs
Below is an excerpt from `app_errors.log` showing the ElevenLabs 503 scenario and subsequent recovery:

```log
2026-01-29 14:51:30,845 - AI_Call_Agent - INFO - --- Processing call for: Bob ---
2026-01-29 14:51:30,845 - retry.strategy - WARNING - Transient error in ElevenLabs: ElevenLabs 503 Service Unavailable. Retrying in 5.39s
2026-01-29 14:51:36,237 - retry.strategy - WARNING - Transient error in ElevenLabs: ElevenLabs 503 Service Unavailable. Retrying in 10.40s
2026-01-29 14:51:46,635 - retry.strategy - ERROR - Max retry attempts (3) reached for ElevenLabs
2026-01-29 14:51:46,637 - circuit_breaker.breaker - ERROR - Circuit for ElevenLabs opened!
2026-01-29 14:51:46,639 - alerts.email_provider - INFO - [Alert] Sending Email to admin@example.com: Service Degradation - Failed to recover ElevenLabs for Bob.
2026-01-29 14:51:46,640 - AI_Call_Agent - INFO - SKIPPING: Bob and moving to next contact.
...
2026-01-29 14:51:58,652 - circuit_breaker.breaker - INFO - Circuit for ElevenLabs moving to HALF_OPEN (timeout elapsed: 12.0s)
2026-01-29 14:51:58,653 - circuit_breaker.breaker - INFO - Circuit for ElevenLabs reset to CLOSED after successful probe
2026-01-29 14:51:58,653 - AI_Call_Agent - INFO - SUCCESS: Call completed for David
```

## Resilience and Maintainability Decisions
- **Decoupled Alerting**: The `AlertManager` uses a provider pattern, making it easy to add Slack or PagerDuty in the future.
- **Circuit Registry**: Ensures that circuit states are consistent across different call processing instances.
- **Config-Driven**: Changing the business logic (e.g., retrying 5 times instead of 3) requires zero code changes, only config updates.
- **Fail-Fast**: Critically avoids wasting expensive LLM or CRM API calls when a core dependency like ElevenLabs is known to be down.
