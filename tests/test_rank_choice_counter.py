import pytest
from src.rank_choicer.rank_choice_counter import RankChoiceCounter


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