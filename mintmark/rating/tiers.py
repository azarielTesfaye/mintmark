"""Graduated and volume per-unit rating."""

from __future__ import annotations

from mintmark.rating.plans import Tier
from mintmark.rating.validate import require_non_negative, validate_tier_bounds


def validate_tiers(tiers: tuple[Tier, ...]) -> None:
    validate_tier_bounds(tuple(tier.up_to for tier in tiers))
    for tier in tiers:
        require_non_negative(tier.price_per_unit, "price")


def rate_graduated(tiers: tuple[Tier, ...], quantity: int) -> int:
    """Price each unit at the tier it falls in.

    ``up_to`` is inclusive. Quantity 0 costs nothing. Units past the previous
    bound, through ``up_to``, use that tier's price. The last tier has no bound.
    """
    validate_tiers(tiers)
    if quantity == 0:
        return 0
    remaining = quantity
    previous = 0
    total = 0
    for tier in tiers:
        if remaining == 0:
            break
        if tier.up_to is None:
            width = remaining
        else:
            width = min(remaining, tier.up_to - previous)
        if width > 0:
            total += width * tier.price_per_unit
            remaining -= width
        if tier.up_to is not None:
            previous = tier.up_to
    return total


def rate_volume(tiers: tuple[Tier, ...], quantity: int) -> int:
    """Price every unit at the single tier the quantity reaches.

    ``up_to`` is inclusive. Quantity 0 costs nothing. A quantity equal to a
    bound stays on that tier; the next unit uses the following tier for the
    whole quantity.
    """
    validate_tiers(tiers)
    if quantity == 0:
        return 0
    selected = tiers[-1]
    for tier in tiers:
        if tier.up_to is None or quantity <= tier.up_to:
            selected = tier
            break
    return quantity * selected.price_per_unit
