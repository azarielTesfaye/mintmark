"""Half-open periods."""

from datetime import date

import pytest

from mintmark.period import Period, overlap_days


def test_day_count_excludes_the_end_date() -> None:
    period = Period(date(2026, 1, 1), date(2026, 2, 1))
    assert period.day_count() == 31


def test_end_must_be_after_start() -> None:
    with pytest.raises(Exception):
        Period(date(2026, 1, 5), date(2026, 1, 5))
    with pytest.raises(Exception):
        Period(date(2026, 1, 6), date(2026, 1, 5))


def test_overlap_counts_only_shared_days() -> None:
    period = Period(date(2026, 1, 1), date(2026, 2, 1))
    covered = Period(date(2026, 1, 17), date(2026, 1, 27))
    assert overlap_days(period, covered) == 10


def test_overlap_outside_the_period_is_zero() -> None:
    period = Period(date(2026, 1, 1), date(2026, 2, 1))
    covered = Period(date(2026, 3, 1), date(2026, 3, 10))
    assert overlap_days(period, covered) == 0


def test_overlap_of_the_whole_period_is_its_day_count() -> None:
    period = Period(date(2026, 1, 1), date(2026, 1, 11))
    assert overlap_days(period, period) == 10
