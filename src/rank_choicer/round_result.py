from dataclasses import dataclass


@dataclass
class RoundResult:
    """Stores the results of a single round of ranked choice counting"""

    round_number: int
    vote_counts: dict[str, int]
    eliminated_option: str | None
    winner: str | None

    def __post_init__(self):
        """Validate the data after initialization"""
        if self.round_number < 0:
            raise ValueError("Round number must be non-negative")

        # Make a copy of vote_counts to prevent external modification
        self.vote_counts = self.vote_counts.copy()
