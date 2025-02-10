from collections import Counter
import random

from .round_result import RoundResult
from .elimination_strategy import EliminationStrategy


class RankChoiceCounter:
    def __init__(self, options: list[str], elimination_strategy: EliminationStrategy = EliminationStrategy.RANDOM) -> None:
        """
        Sets up counter.

        Args:
            options: List of strings representing valid voting options
            elimination_strategy: Strategy to use when there's a tie for elimination
                                (defaults to BATCH - eliminate all tied candidates)

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
        self._elimination_strategy = elimination_strategy
        self._eliminated_options = []

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
        self._eliminated_options = []

    def count_votes(self, votes: dict[str, list[str]]) -> str:
        """
        Counts the votes and returns the winning option

        Args:
            votes: Dictionary of votes to validate

        Raises:
            ValueError: If any vote contains invalid options or is malformed
        """
        self._validate_votes(votes)
        self.clear_results()

        # Make a copy of votes to work with
        current_votes = {voter: prefs.copy() for voter, prefs in votes.items()}

        round_num = 1
        winner = None

        while winner is None:
            round_result = self._calculate_round(round_num, current_votes)
            self._round_results.append(round_result)

            if round_result.winner:
                winner = round_result.winner
                break

            # Remove all eliminated options from vote lists (will be only 1 unless there is a tie)
            for eliminated in round_result.eliminated_options:
                self._eliminated_options.append(eliminated)
                for prefs in current_votes.values():
                    if eliminated in prefs:
                        prefs.remove(eliminated)

            if len(self._eliminated_options) == len(self._options):
                raise ValueError("Ended with a tie. Review round results.")

            round_num += 1

        return winner

    def get_round_results(self) -> list[RoundResult]:
        """
        Get all rounds of processing.

        Returns:
            List of RoundResult objects, one for each round of counting
        """
        return self._round_results.copy()

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
                raise ValueError(
                    f"Invalid options in vote from {voter}: {invalid_options}"
                )

            # Check for duplicates in preferences
            if len(set(preferences)) != len(preferences):
                raise ValueError(f"Duplicate preferences in vote from {voter}")

    def _calculate_round(self, round_number: int, votes: dict[str, list[str]]) -> RoundResult:
        """
        Internal method to calculate a round of rank choice voting

        Args:
            votes: Dictionary of votes to process.
        """
        # Count first preferences
        first_prefs = [prefs[0] for prefs in votes.values() if prefs]
        vote_counts = dict(Counter(first_prefs))

        # Fill in zero counts for options with no votes
        for option in self._options:
            if option not in vote_counts:
                vote_counts[option] = 0

        total_votes = sum(vote_counts.values())
        majority_threshold = total_votes / 2

        # Check for winner
        for option, count in vote_counts.items():
            if count > majority_threshold:
                return RoundResult(
                    round_number=round_number,
                    vote_counts=vote_counts,
                    eliminated_options=None,
                    winner=option
                )

        # No winner, find the candidate(s) that had fewest votes.
        min_votes = min(count for option, count in vote_counts.items() if option not in self._eliminated_options)
        tied_for_last = [option for option, count in vote_counts.items()
                         if count == min_votes and option not in self._eliminated_options]

        if self._elimination_strategy == EliminationStrategy.BATCH:
            # Eliminate all candidates tied for last
            return RoundResult(
                round_number=round_number,
                vote_counts=vote_counts,
                winner=None,
                eliminated_options=tied_for_last
            )
        else:  # RANDOM strategy
            # Randomly choose one candidate to eliminate
            eliminated = random.choice(tied_for_last)
            return RoundResult(
                round_number=round_number,
                vote_counts=vote_counts,
                winner=None,
                eliminated_options=[eliminated]
            )