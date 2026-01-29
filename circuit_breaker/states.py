from enum import Enum, auto

class CircuitState(Enum):
    CLOSED = auto()    # Normal operation
    OPEN = auto()      # Failing fast
    HALF_OPEN = auto() # Testing recovery
