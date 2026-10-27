"""Flat subscription pricing."""

from datetime import date

import pytest

from mintmark import FlatPlan, Period, assemble, quote_usage


def _period(start: tuple[int, int, int], end: tuple[int, int, int]) -> Period:
    return Period(date(*start), date(*end))


def test_full_period_charges_the_price_and_ignores_quantity() -> None:
    period = _period((2026, 1, 1), (2026, 2, 1))
    quote = quote_usage(FlatPlan(2_500), 0, period, period)
    assert quote.amount == 2_500
    assert quote.usage_charge == 2_500
    assert quote.included_units == 0
    assert quote.billed_blocks == 0
    assert quote.floor_uplift == 0
    assert quote.ceiling_reduction == 0
    lines = assemble(quote)
    assert [(line.kind, line.amount) for line in lines] == [("flat", 2_500)]


def test_partial_period_prorates_the_flat_price() -> None:
    period = _period((2026, 1, 1), (2026, 1, 31))
    covered = _period((2026, 1, 1), (2026, 1, 16))
    quote = quote_usage(FlatPlan(3_000), 40, period, covered)
    assert period.day_count() == 30
    assert quote.amount == 1_500


def test_zero_price_emits_no_line() -> None:
    period = _period((2026, 1, 1), (2026, 2, 1))
    quote = quote_usage(FlatPlan(0), 4, period, period)
    assert quote.amount == 0
    assert assemble(quote) == ()


def test_negative_price_or_quantity_raises() -> None:
    period = _period((2026, 1, 1), (2026, 2, 1))
    with pytest.raises(Exception):
        quote_usage(FlatPlan(-1), 1, period, period)
    with pytest.raises(Exception):
        quote_usage(FlatPlan(1), -1, period, period)
