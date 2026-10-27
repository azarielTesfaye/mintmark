"""Volume per-unit tiers."""

from datetime import date

import pytest

from mintmark import GraduatedPlan, Period, Tier, VolumePlan, quote_usage


TIERS = (Tier(10, 5), Tier(None, 3))


def _period(start: tuple[int, int, int], end: tuple[int, int, int]) -> Period:
    return Period(date(*start), date(*end))


def test_zero_quantity_is_free() -> None:
    period = _period((2026, 1, 1), (2026, 2, 1))
    assert quote_usage(VolumePlan(TIERS), 0, period, period).amount == 0


def test_inclusive_bound_prices_every_unit_at_that_tier() -> None:
    period = _period((2026, 1, 1), (2026, 2, 1))
    assert quote_usage(VolumePlan(TIERS), 10, period, period).amount == 50


def test_one_past_the_bound_reprices_the_whole_quantity() -> None:
    period = _period((2026, 1, 1), (2026, 2, 1))
    assert quote_usage(VolumePlan(TIERS), 11, period, period).amount == 33


def test_volume_and_graduated_differ_once_a_later_tier_is_reached() -> None:
    period = _period((2026, 1, 1), (2026, 2, 1))
    quantity = 11
    graduated = quote_usage(GraduatedPlan(TIERS), quantity, period, period).amount
    volume = quote_usage(VolumePlan(TIERS), quantity, period, period).amount
    assert graduated == 53
    assert volume == 33


def test_invalid_tiers_raise() -> None:
    period = _period((2026, 1, 1), (2026, 2, 1))
    with pytest.raises(Exception):
        quote_usage(VolumePlan((Tier(None, 1), Tier(None, 2))), 1, period, period)
