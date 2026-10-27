"""Dispatch a plan to the rater for its kind."""

from __future__ import annotations

from mintmark.period import Period
from mintmark.rating.quote import Quote
from mintmark.rating.standard import quote_flat, quote_graduated, quote_volume


def quote_plan(plan: object, quantity: int, period: Period, covered: Period) -> Quote:
    kind = getattr(plan, "kind", None)
    if kind == "flat":
        return quote_flat(plan, quantity, period, covered)
    if kind == "graduated":
        return quote_graduated(plan, quantity, period, covered)
    if kind == "volume":
        return quote_volume(plan, quantity, period, covered)
    raise ValueError("unknown plan")
