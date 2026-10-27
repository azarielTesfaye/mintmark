"""Quote returned by every rater."""

from __future__ import annotations

from dataclasses import dataclass

from mintmark.invoice.line import Line


@dataclass(frozen=True)
class Quote:
    amount: int
    usage_charge: int
    lines: tuple[Line, ...]
    included_units: int = 0
    billed_blocks: int = 0
    floor_uplift: int = 0
    ceiling_reduction: int = 0
