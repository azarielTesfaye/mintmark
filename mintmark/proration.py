"""Actual-day proration."""

from __future__ import annotations

from mintmark.money import round_div
from mintmark.period import Period, overlap_days


def prorate(amount: int, period: Period, covered: Period) -> int:
    """Prorate ``amount`` by the days ``covered`` shares with ``period``.

    A cover of the whole period returns ``amount`` unchanged. No shared days
    returns 0. Otherwise the result is ``amount * covered_days / period_days``,
    rounded half away from zero.
    """
    if not isinstance(amount, int) or isinstance(amount, bool):
        raise ValueError("amount must be an integer")
    covered_days = overlap_days(period, covered)
    total_days = period.day_count()
    if covered_days <= 0:
        return 0
    if covered_days >= total_days:
        return amount
    return round_div(amount * covered_days, total_days)
