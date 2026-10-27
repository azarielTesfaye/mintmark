"""Invoice lines."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Line:
    kind: str
    amount: int
