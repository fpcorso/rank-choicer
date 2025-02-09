from src.rank_choicer.round_result import RoundResult

class RankChoiceCounter:
    def __init__(self, options: list[str]) -> None:
        """
        Sets up counter.

        Raises:
            ValueError: If options list is empty or contains duplicates
        """
        if not options:
            raise ValueError("Options list cannot be empty")

        # Sanitize options
        sanitized_options = [opt.strip() for opt in options]

        # Check for duplicates by converting to set and comparing lengths
        if len(set(sanitized_options)) != len(sanitized_options):
            raise ValueError("Duplicate options are not allowed")

        # Store a copy of the options to prevent external modification
        self._options = sanitized_options.copy()

        # Initialize results
        self._round_results: list[RoundResult] = []

    @property
    def options(self) -> list[str]:
        """
        Get the current list of valid options.
        """
        return self._options.copy()

    @options.setter
    def options(self, new_options: list[str]) -> None:
        """
        Set new voting options.

        Raises:
            ValueError: If options list is empty or contains duplicates
        """
        if not new_options:
            raise ValueError("Options list cannot be empty")

        if len(set(new_options)) != len(new_options):
            raise ValueError("Duplicate options are not allowed")

        self._options = new_options.copy()

    def add_option(self, option: str) -> None:
        """
        Add a new valid option to the voting options.

        Args:
            option: New option to add

        Raises:
            ValueError: If option already exists
        """
        if option in self._options:
            raise ValueError("Option already exists")

        self._options.append(option)

    def remove_option(self, option: str) -> None:
        """
        Remove an option from the valid voting options.

        Args:
            option: Option to remove

        Raises:
            ValueError: If option doesn't exist
        """
        if option not in self._options:
            raise ValueError("Option does not exist")

        self._options.remove(option)

    def clear_results(self) -> None:
        """Clear all stored round results."""
        self._round_results = []

    def _validate_votes(self, votes: dict[str, list[str]]) -> None:
        """
        Internal method to validate votes against current options.

        Args:
            votes: Dictionary of votes to validate

        Raises:
            ValueError: If any vote contains invalid options or is malformed
        """
        options_set = set(self._options.copy())
        for voter, preferences in votes.items():
            if not isinstance(voter, str) or not voter.strip():
                raise ValueError("Invalid voter")

            if len(preferences) > len(self._options):
                raise ValueError(f"Too many preferences from {voter}")

            if not preferences:
                raise ValueError(f"Empty preference list from {voter}")

            # Check for None or invalid types
            if any(not isinstance(pref, str) for pref in preferences):
                raise ValueError(f"Invalid vote type from {voter}")

            # Check that all preferences are valid options
            invalid_options = set(preferences) - options_set
            if invalid_options:
                raise ValueError(f"Invalid options in vote from {voter}: {invalid_options}")

            # Check for duplicates in preferences
            if len(set(preferences)) != len(preferences):
                raise ValueError(f"Duplicate preferences in vote from {voter}")