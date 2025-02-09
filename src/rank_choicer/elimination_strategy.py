from enum import Enum, auto

class EliminationStrategy(Enum):
    """Strategy to use when there's a tie for elimination"""
    BATCH = auto()    # Eliminate all candidates tied for last place
    RANDOM = auto()   # Randomly choose one candidate to eliminate from those tied