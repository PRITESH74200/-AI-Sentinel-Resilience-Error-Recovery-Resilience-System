import logging
from typing import List, Dict
from services.elevenlabs import ElevenLabsService
from services.llm import LLMService
from services.crm import CRMService
from retry.strategy import RetryStrategy
from circuit_breaker.registry import CircuitBreakerRegistry
from circuit_breaker.states import CircuitState
from exceptions.base import TransientError, PermanentError, AgentException
from app_logging.manager import LogManager
from alerts.manager import AlertManager
from config.settings import SERVICE_CONFIGS

logger = logging.getLogger(__name__)

class CallProcessor:
    def __init__(self, log_manager: LogManager, alert_manager: AlertManager):
        self.log_manager = log_manager
        self.alert_manager = alert_manager
        
        # Initialize services
        self.eleven_labs = ElevenLabsService()
        self.llm = LLMService()
        self.crm = CRMService()
        
        self.services = {
            "ElevenLabs": self.eleven_labs,
            "LLM": self.llm,
            "CRM": self.crm
        }

    def process_queue(self, contacts: List[Dict]):
        self.log_manager.info(f"Starting to process {len(contacts)} contacts...")
        
        for contact in contacts:
            try:
                self._process_single_call(contact)
            except Exception as e:
                # Top level catch to ensure we don't block the entire system
                self.log_manager.base_logger.critical(f"Unexpected failure processing {contact['name']}: {str(e)}")
                continue

    def _process_single_call(self, contact: Dict):
        name = contact["name"]
        self.log_manager.info(f"--- Processing call for: {name} ---")

        try:
            # 1. Generate script via LLM
            script = self._execute_with_resilience("LLM", self.llm.process, f"Generate intro for {name}")
            
            # 2. Convert to Speech via ElevenLabs
            audio = self._execute_with_resilience("ElevenLabs", self.eleven_labs.process, script)
            
            # 3. Update CRM
            self._execute_with_resilience("CRM", self.crm.process, {"contact": name, "status": "completed"})
            
            self.log_manager.info(f"SUCCESS: Call completed for {name}")

        except PermanentError as e:
            self.log_manager.error(e.service_name, "PERMANENT", str(e))
            self.alert_manager.trigger("Critical Process Failure", f"Permanent error in {e.service_name} for {name}: {str(e)}")
            self.log_manager.info(f"SKIPPING: {name} due to permanent error.")

        except AgentException as e:
            # This handles cases where circuit is open or max retries reached
            self.log_manager.error(e.service_name, "FATAL_RECOVERY", str(e))
            self.alert_manager.trigger("Service Degradation", f"Failed to recover {e.service_name} for {name}. Error: {str(e)}")
            self.log_manager.info(f"SKIPPING: {name} and moving to next contact.")

    def _execute_with_resilience(self, service_name: str, func, *args, **kwargs):
        config = SERVICE_CONFIGS[service_name]
        retry_settings = config["retry"]
        
        retry_strategy = RetryStrategy(
            max_attempts=retry_settings["max_attempts"],
            initial_delay=retry_settings["initial_delay"],
            exponential_base=retry_settings["exponential_base"]
        )
        
        breaker = CircuitBreakerRegistry.get_breaker(service_name)
        
        # Circuit Breaker wraps the execution
        return breaker.call(
            # Retry Strategy wraps the actual call
            retry_strategy.execute, func, *args, **kwargs
        )
