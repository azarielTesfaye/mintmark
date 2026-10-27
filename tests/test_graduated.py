"""Graduated per-unit tiers."""

from datetime import date

import pytest

from mintmark import GraduatedPlan, Period, Tier, quote_usage


TIERS = (Tier(10, 5), Tier(None, 3))


def _period(start: tuple[int, int, int], end: tuple[int, int, int]) -> Period:
    return Period(date(*start), date(*end))


def test_zero_quantity_is_free() -> None:
    period = _period((2026, 1, 1), (2026, 2, 1))
    assert quote_usage(GraduatedPlan(TIERS), 0, period, period).amount == 0


def test_inclusive_bound_stays_on_that_tier() -> None:
    period = _period((2026, 1, 1), (2026, 2, 1))
    assert quote_usage(GraduatedPlan(TIERS), 10, period, period).amount == 50


def test_the_next_unit_uses_the_following_tier_only_for_itself() -> None:
    period = _period((2026, 1, 1), (2026, 2, 1))
    assert quote_usage(GraduatedPlan(TIERS), 11, period, period).amount == 53


def test_partial_period_prorates_after_the_tier_walk() -> None:
    period = _period((2026, 1, 1), (2026, 1, 11))
    covered = _period((2026, 1, 1), (2026, 1, 6))
    quote = quote_usage(GraduatedPlan(TIERS), 10, period, covered)
    assert quote.amount == 25
    assert quote.usage_charge == 25


def test_bounds_must_end_unbounded_and_increase() -> None:
    period = _period((2026, 1, 1), (2026, 2, 1))
    with pytest.raises(Exception):
        quote_usage(GraduatedPlan((Tier(10, 5),)), 1, period, period)
    with pytest.raises(Exception):
        quote_usage(GraduatedPlan((Tier(5, 1), Tier(5, 1), Tier(None, 1))), 1, period, period)
    with pytest.raises(Exception):
        quote_usage(GraduatedPlan((Tier(10, -1), Tier(None, 1))), 1, period, period)
    with pytest.raises(Exception):
        quote_usage(GraduatedPlan(()), 1, period, period)
