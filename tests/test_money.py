"""Money rounding and allocation."""

from mintmark.money import allocate, round_div


def test_half_away_from_zero_on_an_exact_half() -> None:
    assert round_div(1, 2) == 1
    assert round_div(5, 2) == 3
    assert round_div(2, 4) == 1


def test_half_away_from_zero_below_and_above_the_half() -> None:
    assert round_div(1, 4) == 0
    assert round_div(3, 4) == 1
    assert round_div(10, 3) == 3


def test_negative_half_rounds_away_from_zero() -> None:
    assert round_div(-1, 2) == -1
    assert round_div(-1, 4) == 0
    assert round_div(-3, 2) == -2
    assert round_div(-5, 2) == -3


def test_allocate_parts_sum_to_the_total() -> None:
    parts = allocate(5, [2, 1])
    assert parts == [3, 2]
    assert sum(parts) == 5


def test_equal_remainders_favor_the_earlier_weight() -> None:
    parts = allocate(10, [1, 1, 1])
    assert parts == [4, 3, 3]
    assert sum(parts) == 10


def test_zero_total_allocates_zeros() -> None:
    assert allocate(0, [2, 5, 1]) == [0, 0, 0]


def test_negative_total_negates_the_positive_split() -> None:
    assert allocate(-10, [1, 1, 1]) == [-4, -3, -3]
    assert sum(allocate(-5, [2, 1])) == -5


def test_allocate_rejects_empty_or_non_positive_weights() -> None:
    import pytest

    with pytest.raises(Exception):
        allocate(5, [])
    with pytest.raises(Exception):
        allocate(5, [0, 0])
    with pytest.raises(Exception):
        allocate(5, [1, -1])
