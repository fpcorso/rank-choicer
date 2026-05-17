import pytest

from src.rank_choicer.round_result import RoundResult


def test_round_result_initialization():
    """Test basic initialization of RoundResult"""
    vote_counts = {"Option A": 10, "Option B": 5}
    result = RoundResult(
        round_number=1,
        vote_counts=vote_counts,
        eliminated_options=["Option B"],
        winner=None,
    )

    assert result.round_number == 1
    assert result.vote_counts == vote_counts
    assert result.eliminated_options == ["Option B"]
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


def test_invalid_round_number_negative():
    """Test that a negative round number raises ValueError"""
    with pytest.raises(ValueError) as exc_info:
        RoundResult(-1, {"A": 10}, None, None)
    assert "Round number must be a positive integer" in str(exc_info.value)


def test_invalid_round_number_zero():
    """Test that round number 0 raises ValueError"""
    with pytest.raises(ValueError) as exc_info:
        RoundResult(0, {"A": 10}, None, None)
    assert "Round number must be a positive integer" in str(exc_info.value)


def test_to_dict_with_winner():
    """Test that to_dict returns correct structure when round has a winner"""
    result = RoundResult(
        round_number=2,
        vote_counts={"Option A": 3, "Option B": 2},
        winner="Option A",
        eliminated_options=None,
    )
    result_dict = result.to_dict()

    assert isinstance(result_dict, dict)
    assert result_dict["round_number"] == 2
    assert result_dict["vote_counts"] == {"Option A": 3, "Option B": 2}
    assert result_dict["winner"] == "Option A"
    assert result_dict["eliminated_options"] is None


def test_to_dict_with_elimination():
    """Test that to_dict returns correct structure when round has eliminations"""
    result = RoundResult(
        round_number=1,
        vote_counts={"Option A": 3, "Option B": 1, "Option C": 1},
        winner=None,
        eliminated_options=["Option B", "Option C"],
    )
    result_dict = result.to_dict()

    assert isinstance(result_dict, dict)
    assert result_dict["round_number"] == 1
    assert result_dict["vote_counts"] == {"Option A": 3, "Option B": 1, "Option C": 1}
    assert result_dict["winner"] is None
    assert result_dict["eliminated_options"] == ["Option B", "Option C"]
