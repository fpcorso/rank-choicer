
class RankChoiceCounter:
    def __init__(self, options: list[str]) -> None:
        """
        Sets up counter.

        Raises:
            ValueError: If options list is empty or contains duplicates
        """
        if not options:
            raise ValueError("Options list cannot be empty")

        # Check for duplicates by converting to set and comparing lengths
        if len(set(options)) != len(options):
            raise ValueError("Duplicate options are not allowed")

        # Store a copy of the options to prevent external modification
        self._options = options.copy()

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