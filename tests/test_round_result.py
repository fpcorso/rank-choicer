import pytest
from src.rank_choicer.round_result import RoundResult


def test_round_result_initialization():
    """Test basic initialization of RoundResult"""
    vote_counts = {"Option A": 10, "Option B": 5}
    result = RoundResult(
        round_number=1,
        vote_counts=vote_counts,
        eliminated_option="Option B",
        winner=None
    )

    assert result.round_number == 1
    assert result.vote_counts == vote_counts
    assert result.eliminated_option == "Option B"
    assert result.winner is None


def test_round_result_equality():
    """Test that two RoundResults with same values are equal"""
    result1 = RoundResult(1, {"A": 10, "B": 5}, "B", None)
    result2 = RoundResult(1, {"A": 10, "B": 5}, "B", None)
    result3 = RoundResult(1, {"A": 10, "B": 6}, "B", None)  # Different vote count

    assert result1 == result2
    assert result1 != result3


def test_vote_counts_immutability():
    """Test that modifying vote_counts after creation doesn't affect the original"""
    vote_counts = {"Option A": 10, "Option B": 5}
    result = RoundResult(1, vote_counts, None, None)

    # Modify the original vote_counts
    vote_counts["Option A"] = 20

    # Result should maintain the original values
    assert result.vote_counts["Option A"] == 10


def test_invalid_round_number():
    """Test that round_number must be a positive integer"""
    with pytest.raises(ValueError):
        RoundResult(-1, {"A": 10}, None, None)