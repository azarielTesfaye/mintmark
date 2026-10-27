"""Invoice assembly."""

from __future__ import annotations

from mintmark.invoice.line import Line
from mintmark.rating.quote import Quote


def assemble(quote: Quote) -> tuple[Line, ...]:
    """Return the invoice lines on ``quote``."""
    return quote.lines
