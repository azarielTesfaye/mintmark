"""Quotes for flat, graduated, and volume plans."""

from __future__ import annotations

from mintmark.invoice.line import Line
from mintmark.period import Period
from mintmark.proration import prorate
from mintmark.rating.plans import FlatPlan, GraduatedPlan, VolumePlan
from mintmark.rating.quote import Quote
from mintmark.rating.tiers import rate_graduated, rate_volume
from mintmark.rating.validate import require_non_negative


def _finish(kind: str, raw: int, period: Period, covered: Period) -> Quote:
    amount = prorate(raw, period, covered)
    lines = () if amount == 0 else (Line(kind, amount),)
    return Quote(amount=amount, usage_charge=amount, lines=lines)


def quote_flat(plan: FlatPlan, quantity: int, period: Period, covered: Period) -> Quote:
    require_non_negative(plan.price, "price")
    require_non_negative(quantity, "quantity")
    return _finish(plan.kind, plan.price, period, covered)


def quote_graduated(plan: GraduatedPlan, quantity: int, period: Period, covered: Period) -> Quote:
    require_non_negative(quantity, "quantity")
    return _finish(plan.kind, rate_graduated(plan.tiers, quantity), period, covered)


def quote_volume(plan: VolumePlan, quantity: int, period: Period, covered: Period) -> Quote:
    require_non_negative(quantity, "quantity")
    return _finish(plan.kind, rate_volume(plan.tiers, quantity), period, covered)
