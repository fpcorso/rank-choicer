from dataclasses import asdict, dataclass


@dataclass
class RoundResult:
    """Stores the results of a single round of ranked choice counting"""

    round_number: int
    vote_counts: dict[str, int]
    winner: str | None
    eliminated_options: list[str] | None

    def __post_init__(self):
        """Validate the data after initialization"""
        if self.round_number < 1:
            raise ValueError("Round number must be a positive integer")

        # Make a copy of vote_counts to prevent external modification
        self.vote_counts = self.vote_counts.copy()

    def to_dict(self) -> dict:
        """Return the round result as a dictionary."""
        return asdict(self)
