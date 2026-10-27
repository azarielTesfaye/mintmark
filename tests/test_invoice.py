"""Invoice lines and reversals."""

from datetime import date

from mintmark import FlatPlan, GraduatedPlan, Period, Tier, VolumePlan, assemble, quote_usage, reverse


def _period(start: tuple[int, int, int], end: tuple[int, int, int]) -> Period:
    return Period(date(*start), date(*end))


def test_each_plan_emits_one_line_named_for_its_kind() -> None:
    period = _period((2026, 1, 1), (2026, 2, 1))
    tiers = (Tier(10, 5), Tier(None, 3))
    flat = assemble(quote_usage(FlatPlan(100), 1, period, period))
    graduated = assemble(quote_usage(GraduatedPlan(tiers), 2, period, period))
    volume = assemble(quote_usage(VolumePlan(tiers), 2, period, period))
    assert [(line.kind, line.amount) for line in flat] == [("flat", 100)]
    assert [(line.kind, line.amount) for line in graduated] == [("graduated", 10)]
    assert [(line.kind, line.amount) for line in volume] == [("volume", 10)]


def test_a_zero_charge_emits_no_line() -> None:
    period = _period((2026, 1, 1), (2026, 2, 1))
    tiers = (Tier(10, 5), Tier(None, 3))
    assert assemble(quote_usage(GraduatedPlan(tiers), 0, period, period)) == ()


def test_reversal_negates_lines_and_a_second_reversal_restores_them() -> None:
    period = _period((2026, 1, 1), (2026, 2, 1))
    lines = assemble(quote_usage(FlatPlan(80), 3, period, period))
    negated = reverse(lines)
    assert [(line.kind, line.amount) for line in negated] == [("flat", -80)]
    assert [(line.kind, line.amount) for line in reverse(negated)] == [("flat", 80)]


def test_line_amounts_sum_to_the_quote() -> None:
    period = _period((2026, 1, 1), (2026, 1, 11))
    covered = _period((2026, 1, 1), (2026, 1, 6))
    quote = quote_usage(FlatPlan(100), 1, period, covered)
    assert sum(line.amount for line in assemble(quote)) == quote.amount


def test_unknown_plan_raises() -> None:
    import pytest

    period = _period((2026, 1, 1), (2026, 2, 1))

    class Other:
        kind = "other"

    with pytest.raises(Exception):
        quote_usage(Other(), 1, period, period)
