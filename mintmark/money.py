"""Integer minor-unit arithmetic."""

from __future__ import annotations


def round_div(numerator: int, denominator: int) -> int:
    """Divide and round half away from zero.

    ``denominator`` must be positive. An exact half rounds away from zero.
    """
    if not isinstance(denominator, int) or isinstance(denominator, bool) or denominator <= 0:
        raise ValueError("denominator must be a positive integer")
    if not isinstance(numerator, int) or isinstance(numerator, bool):
        raise ValueError("numerator must be an integer")
    if numerator < 0:
        return -round_div(-numerator, denominator)
    return (numerator + denominator // 2) // denominator


def allocate(total: int, weights: list[int] | tuple[int, ...]) -> list[int]:
    """Split ``total`` across ``weights`` so the parts sum to ``total``.

    Each part starts as the floor of its exact share. Leftover units go to the
    largest remainders. Equal remainders favor the earlier weight. A negative
    total is the negation of allocating its absolute value, so the parts still
    sum to ``total``.
    """
    if not isinstance(total, int) or isinstance(total, bool):
        raise ValueError("total must be an integer")
    if not weights:
        raise ValueError("weights are required")
    if any(not isinstance(weight, int) or isinstance(weight, bool) or weight < 0 for weight in weights):
        raise ValueError("weights must be non-negative integers")
    weight_sum = sum(weights)
    if weight_sum == 0:
        raise ValueError("at least one weight must be positive")
    if total < 0:
        return [-part for part in allocate(-total, weights)]
    floors: list[int] = []
    remainders: list[int] = []
    for weight in weights:
        numerator = total * weight
        floors.append(numerator // weight_sum)
        remainders.append(numerator % weight_sum)
    leftover = total - sum(floors)
    order = sorted(range(len(weights)), key=lambda index: (-remainders[index], index))
    for index in order[:leftover]:
        floors[index] += 1
    return floors
