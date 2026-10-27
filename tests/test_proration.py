"""Actual-day proration."""

from datetime import date

from mintmark.period import Period
from mintmark.proration import prorate


def _period(start: tuple[int, int, int], end: tuple[int, int, int]) -> Period:
    return Period(date(*start), date(*end))


def test_full_cover_returns_the_amount_unchanged() -> None:
    period = _period((2026, 1, 1), (2026, 2, 1))
    assert prorate(62, period, period) == 62


def test_no_shared_days_returns_zero() -> None:
    period = _period((2026, 1, 1), (2026, 2, 1))
    covered = _period((2026, 3, 1), (2026, 3, 5))
    assert prorate(62, period, covered) == 0


def test_partial_cover_uses_actual_days_and_half_away() -> None:
    period = _period((2026, 1, 1), (2026, 1, 3))
    covered = _period((2026, 1, 1), (2026, 1, 2))
    assert period.day_count() == 2
    assert prorate(1, period, covered) == 1


def test_partial_cover_below_a_half_rounds_toward_zero() -> None:
    period = _period((2026, 1, 1), (2026, 1, 5))
    covered = _period((2026, 1, 1), (2026, 1, 2))
    assert prorate(1, period, covered) == 0


def test_negative_amount_rounds_away_from_zero() -> None:
    period = _period((2026, 1, 1), (2026, 1, 3))
    covered = _period((2026, 1, 1), (2026, 1, 2))
    assert prorate(-1, period, covered) == -1
