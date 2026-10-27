"""Invoice reversal."""

from __future__ import annotations

from mintmark.invoice.line import Line


def reverse(lines: tuple[Line, ...] | list[Line]) -> tuple[Line, ...]:
    """Negate each emitted line without rating usage again."""
    return tuple(Line(kind=line.kind, amount=-line.amount) for line in lines)
