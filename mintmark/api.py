"""Public rating entry point."""

from __future__ import annotations

from mintmark.period import Period
from mintmark.rating.quote import Quote
from mintmark.rating.registry import quote_plan
from mintmark.rating.validate import require_non_negative


def quote_usage(plan: object, quantity: int, period: Period, covered: Period) -> Quote:
    """Quote ``quantity`` on ``plan`` for ``period``, covering ``covered``."""
    require_non_negative(quantity, "quantity")
    return quote_plan(plan, quantity, period, covered)
