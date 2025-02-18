import pytest
from src.rank_choicer.rank_choice_counter import RankChoiceCounter
from src.rank_choicer.elimination_strategy import EliminationStrategy


def test_initialize_with_valid_options():
    """Test that counter initializes correctly with valid options"""
    options = ["Option A", "Option B", "Option C"]
    counter = RankChoiceCounter(options)
    assert counter.options == options


def test_initialize_with_empty_options():
    """Test that counter raises error when initialized with empty list"""
    with pytest.raises(ValueError) as exc_info:
        RankChoiceCounter([])
    assert "Options list cannot be empty" in str(exc_info.value)


def test_initialize_with_duplicate_options():
    """Test that counter raises error when initialized with duplicate options"""
    options = ["Option A", "Option B", "Option A"]
    with pytest.raises(ValueError) as exc_info:
        RankChoiceCounter(options)
    assert "Duplicate options are not allowed" in str(exc_info.value)


def test_add_valid_option():
    """Test adding a new valid option"""
    counter = RankChoiceCounter(["Option A", "Option B"])
    counter.add_option("Option C")
    assert "Option C" in counter.options
    assert len(counter.options) == 3


def test_add_duplicate_option():
    """Test that adding duplicate option raises error"""
    counter = RankChoiceCounter(["Option A", "Option B"])
    with pytest.raises(ValueError) as exc_info:
        counter.add_option("Option A")
    assert "Option already exists" in str(exc_info.value)


def test_remove_existing_option():
    """Test removing an existing option"""
    counter = RankChoiceCounter(["Option A", "Option B", "Option C"])
    counter.remove_option("Option B")
    assert "Option B" not in counter.options
    assert len(counter.options) == 2


def test_remove_nonexistent_option():
    """Test that removing nonexistent option raises error"""
    counter = RankChoiceCounter(["Option A", "Option B"])
    with pytest.raises(ValueError) as exc_info:
        counter.remove_option("Option C")
    assert "Option does not exist" in str(exc_info.value)


def test_set_new_options():
    """Test setting entirely new set of options"""
    counter = RankChoiceCounter(["Option A", "Option B"])
    new_options = ["Choice 1", "Choice 2", "Choice 3"]
    counter.options = new_options
    assert counter.options == new_options


def test_options_immutability():
    """Test that the options property returns a copy of the options list"""
    options = ["Option A", "Option B"]
    counter = RankChoiceCounter(options)

    # Try to modify the returned options
    counter_options = counter.options
    counter_options.append("Option C")

    # Original options should be unchanged
    assert "Option C" not in counter.options
    assert len(counter.options) == 2


def test_validate_votes_valid_input():
    """Test that valid votes pass validation"""
    counter = RankChoiceCounter(["Option A", "Option B", "Option C"])
    votes = {
        "voter1": ["Option A", "Option B", "Option C"],
        "voter2": ["Option B", "Option C", "Option A"],
    }
    # Should not raise any exceptions
    counter._validate_votes(votes)


def test_validate_votes_invalid_option():
    """Test that votes containing invalid options raise ValueError"""
    counter = RankChoiceCounter(["Option A", "Option B", "Option C"])
    votes = {
        "voter1": ["Option A", "Option B", "Option C"],
        "voter2": ["Option D", "Option B", "Option A"],  # Option D doesn't exist
    }
    with pytest.raises(ValueError) as exc_info:
        counter._validate_votes(votes)
    assert "Invalid options in vote from voter2" in str(exc_info.value)


def test_validate_votes_duplicate_preferences():
    """Test that votes containing duplicate preferences raise ValueError"""
    counter = RankChoiceCounter(["Option A", "Option B", "Option C"])
    votes = {"voter1": ["Option A", "Option B", "Option A"]}  # Option A appears twice
    with pytest.raises(ValueError) as exc_info:
        counter._validate_votes(votes)
    assert "Duplicate preferences in vote from voter1" in str(exc_info.value)


def test_validate_votes_empty_preferences():
    """Test that empty preference list raises ValueError"""
    counter = RankChoiceCounter(["Option A", "Option B", "Option C"])
    votes = {"voter1": []}
    with pytest.raises(ValueError) as exc_info:
        counter._validate_votes(votes)
    assert "Empty preference list from voter1" in str(exc_info.value)


def test_validate_votes_none_preferences():
    """Test that None in preferences raises ValueError"""
    counter = RankChoiceCounter(["Option A", "Option B", "Option C"])
    votes = {"voter1": ["Option A", None, "Option B"]}
    with pytest.raises(ValueError) as exc_info:
        counter._validate_votes(votes)
    assert "Invalid vote type from voter1" in str(exc_info.value)


def test_validate_votes_invalid_voter_id():
    """Test that invalid voter IDs raise ValueError"""
    counter = RankChoiceCounter(["Option A", "Option B", "Option C"])
    votes = {"": ["Option A", "Option B", "Option C"]}  # Empty voter ID
    with pytest.raises(ValueError) as exc_info:
        counter._validate_votes(votes)
    assert "Invalid voter" in str(exc_info.value)


def test_validate_votes_too_many_preferences():
    """Test that having more preferences than options raises ValueError"""
    counter = RankChoiceCounter(["Option A", "Option B"])
    votes = {
        "voter1": ["Option A", "Option B", "Option B"]  # More preferences than options
    }
    with pytest.raises(ValueError) as exc_info:
        counter._validate_votes(votes)
    assert "Too many preferences from voter1" in str(exc_info.value)


def test_validate_votes_partial_preferences():
    """Test that partial preference lists are valid"""
    counter = RankChoiceCounter(["Option A", "Option B", "Option C"])
    votes = {
        "voter1": ["Option A", "Option B"],  # Only two preferences
        "voter2": ["Option C"],  # Only one preference
    }
    # Should not raise any exceptions
    counter._validate_votes(votes)


def test_single_round_clear_winner():
    """Test round calculation when there's a clear majority winner"""
    counter = RankChoiceCounter(["A", "B", "C"])
    votes = {"v1": ["A", "B", "C"], "v2": ["A", "C"], "v3": ["A", "B"]}
    result = counter._calculate_round(1, votes)

    assert result.vote_counts == {"A": 3, "B": 0, "C": 0}
    assert result.winner == "A"
    assert result.eliminated_options is None


def test_single_round_no_winner():
    """Test round calculation when no candidate has majority"""
    counter = RankChoiceCounter(["A", "B", "C"])
    votes = {
        "v1": ["A", "B", "C"],
        "v2": ["A", "C", "B"],
        "v3": ["B", "C", "A"],
        "v4": ["B", "C", "A"],
        "v5": ["C", "B", "A"],
    }
    result = counter._calculate_round(1, votes)

    assert result.vote_counts == {"A": 2, "B": 2, "C": 1}
    assert result.winner is None
    assert result.eliminated_options == ["C"]


def test_single_round_with_eliminated_candidates():
    """Test round calculation with some candidates already eliminated"""
    counter = RankChoiceCounter(["A", "B", "C"])
    # C was eliminated in previous round
    votes = {
        "v1": ["A", "B"],
        "v2": ["A", "B"],
        "v3": ["B", "A"],
        "v4": ["B", "A"],
        "v5": ["B", "A"],
    }
    result = counter._calculate_round(2, votes)

    assert result.vote_counts == {
        "A": 2,
        "B": 3,
        "C": 0,
    }  # C should still be present in totals
    assert result.winner == "B"
    assert result.eliminated_options is None


def test_count_votes_immediate_winner():
    """Test when a candidate wins in the first round"""
    counter = RankChoiceCounter(["A", "B", "C"])
    votes = {"v1": ["A", "B", "C"], "v2": ["A", "C", "B"], "v3": ["A", "B", "C"]}
    winner = counter.count_votes(votes)
    results = counter.get_round_results()

    assert winner == "A"
    assert len(results) == 1
    assert results[0].winner == "A"
    assert results[0].round_number == 1


def test_count_votes_two_rounds():
    """Test when winner is determined after one elimination"""
    counter = RankChoiceCounter(["A", "B", "C"])
    votes = {
        "v1": ["A", "B", "C"],
        "v2": ["B", "A", "C"],
        "v3": ["C", "A", "B"],
        "v4": ["A", "C", "B"],
        "v5": ["B", "C", "A"],
    }
    winner = counter.count_votes(votes)
    results = counter.get_round_results()

    assert winner == "A"
    assert len(results) == 2
    # First round should have eliminated C
    assert results[0].winner is None
    assert results[0].eliminated_options == ["C"]
    assert results[0].round_number == 1
    # Second round should have a winner
    assert results[1].winner == winner
    assert results[1].round_number == 2


def test_count_votes_three_rounds():
    """Test when winner is determined after two eliminations"""
    counter = RankChoiceCounter(["A", "B", "C", "D"])
    votes = {
        "v1": ["A", "B", "C", "D"],
        "v2": ["A", "B", "C", "D"],
        "v3": ["A", "C", "D", "B"],
        "v4": ["B", "D", "A", "C"],
        "v5": ["B", "A", "C", "D"],
        "v6": ["C", "A", "B", "D"],
        "v7": ["C", "A", "B", "D"],
        "v8": ["D", "B", "A", "C"],
    }
    winner = counter.count_votes(votes)
    results = counter.get_round_results()

    assert winner == "A"
    assert len(results) == 3
    # First round should have eliminated D
    assert results[0].winner is None
    assert results[0].eliminated_options == ["D"]
    assert results[0].round_number == 1
    # Second round should have eliminated C
    assert results[1].winner is None
    assert results[1].eliminated_options == ["C"]
    assert results[1].round_number == 2
    # Third round should have a winner
    assert results[2].winner == winner
    assert results[2].round_number == 3


def test_batch_elimination_strategy():
    """Test that batch elimination works correctly"""
    counter = RankChoiceCounter(
        ["A", "B", "C", "D"], elimination_strategy=EliminationStrategy.BATCH
    )
    votes = {
        "v1": ["A", "B", "C", "D"],
        "v2": ["A", "B", "C", "D"],
        "v3": ["B", "C", "D", "A"],
        "v4": ["B", "D", "A", "C"],
        "v5": ["C", "A", "B", "D"],
        "v6": ["D", "A", "B", "C"],
    }
    counter.count_votes(votes)
    first_round = counter.get_round_results()[0]

    # Should eliminate both C and D if they're tied
    assert len(first_round.eliminated_options) > 1
    assert first_round.eliminated_options == ["C", "D"]


def test_random_elimination_strategy():
    """Test that random elimination works correctly"""
    counter = RankChoiceCounter(
        ["A", "B", "C", "D"], elimination_strategy=EliminationStrategy.RANDOM
    )
    votes = {
        "v1": ["A", "B", "C", "D"],
        "v2": ["A", "B", "C", "D"],
        "v3": ["B", "C", "D", "A"],
        "v4": ["B", "D", "A", "C"],
        "v5": ["C", "A", "B", "D"],
        "v6": ["D", "A", "B", "C"],
    }
    counter.count_votes(votes)
    first_round = counter.get_round_results()[0]

    # Should only eliminate one candidate
    assert len(first_round.eliminated_options) == 1


def test_tie_batch_elimination_strategy():
    """Test a final tie on batch elimination works correctly"""
    counter = RankChoiceCounter(
        ["A", "B", "C", "D"], elimination_strategy=EliminationStrategy.BATCH
    )
    votes = {
        "v1": ["A", "B", "C", "D"],
        "v2": ["A", "B", "C", "D"],
        "v3": ["A", "C", "D", "B"],
        "v4": ["B", "D", "A", "C"],
        "v5": ["B", "A", "C", "D"],
        "v6": ["C", "A", "B", "D"],
        "v7": ["C", "B", "A", "D"],
        "v8": ["D", "B", "A", "C"],
    }

    with pytest.raises(ValueError) as exc_info:
        counter.count_votes(votes)
    assert "Ended with a tie. Review round results." in str(exc_info.value)
