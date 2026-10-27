"""Shared checks for quantities, prices, and tier bounds."""

from __future__ import annotations


def require_non_negative(value: int, label: str) -> None:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ValueError(f"{label} must be a non-negative integer")


def validate_tier_bounds(bounds: tuple[int | None, ...]) -> None:
    """Require a non-empty ladder whose only unbounded step is the last one.

    Each earlier ``up_to`` is an inclusive bound and must be strictly greater
    than the bound before it. The first bound must be at least 1.
    """
    if not bounds:
        raise ValueError("at least one tier is required")
    previous = 0
    last_index = len(bounds) - 1
    for index, bound in enumerate(bounds):
        if index == last_index:
            if bound is not None:
                raise ValueError("the last tier must be unbounded")
            continue
        if not isinstance(bound, int) or isinstance(bound, bool) or bound <= previous:
            raise ValueError("tier bounds must increase")
        previous = bound
