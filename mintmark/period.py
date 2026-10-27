"""Half-open civil date periods."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Period:
    """A half-open range of civil dates, ``[start, end)``."""

    start: date
    end: date

    def __post_init__(self) -> None:
        if not isinstance(self.start, date) or not isinstance(self.end, date):
            raise ValueError("period bounds must be dates")
        if self.end <= self.start:
            raise ValueError("period end must be after start")

    def day_count(self) -> int:
        return (self.end - self.start).days


def overlap_days(period: Period, covered: Period) -> int:
    """Return how many days fall in both half-open periods."""
    start = period.start if period.start >= covered.start else covered.start
    end = period.end if period.end <= covered.end else covered.end
    if end <= start:
        return 0
    return (end - start).days
