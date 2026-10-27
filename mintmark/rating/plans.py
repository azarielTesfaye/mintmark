"""Plans that already ship with the library."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Tier:
    """Inclusive upper bound on quantity. ``up_to is None`` means unbounded."""

    up_to: int | None
    price_per_unit: int


@dataclass(frozen=True)
class FlatPlan:
    price: int
    kind: str = "flat"


@dataclass(frozen=True)
class GraduatedPlan:
    tiers: tuple[Tier, ...]
    kind: str = "graduated"


@dataclass(frozen=True)
class VolumePlan:
    tiers: tuple[Tier, ...]
    kind: str = "volume"
