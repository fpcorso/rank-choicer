
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