# mintmark

mintmark rates usage and builds invoices in integer minor units. Amounts are
never floating point. A period is a half-open range of civil dates, `[start, end)`,
and a charge that does not cover the whole period is prorated by actual days.

## Money

`round_div` divides two integers and rounds half away from zero. `allocate`
splits a total by weights so the parts sum to the total: each part starts as
the floor of its share, leftover units go to the largest remainders, and equal
remainders favor the earlier weight.

## Periods and proration

`Period.day_count` is the number of civil days in `[start, end)`. Shared days
between a billing period and the days a subscription covers are the overlap of
those two ranges. `prorate(amount, period, covered)` returns `amount` unchanged
when the covered days include the whole period, returns 0 when they share no
days, and otherwise returns `amount * covered_days / period_days`, rounded half
away from zero.

## Plans

Pass a plan to `quote_usage(plan, quantity, period, covered)`.

- `FlatPlan(price)` charges `price` for the period. Quantity does not change
  the price, including when quantity is 0. A partial cover prorates the price.
- `GraduatedPlan(tiers)` prices each unit at the tier it falls in. `Tier.up_to`
  is an inclusive bound. The last tier is unbounded (`up_to is None`). Quantity
  0 costs nothing. A unit past a bound is priced at the next tier; earlier units
  keep their own tier's price.
- `VolumePlan(tiers)` uses the same bounds, but every unit is priced at the
  single tier the quantity reaches. A quantity equal to `up_to` stays on that
  tier. The next unit moves the whole quantity onto the following tier.

Bounded tiers must strictly increase, the first bound must be at least 1, and
only the last tier is unbounded. Prices and quantities are non-negative
integers. A negative quantity, a negative price, or a broken tier ladder raises.

A zero charge produces an empty invoice. Any other charge produces one line
whose kind is `flat`, `graduated`, or `volume` and whose amount is the quote.
`reverse` negates those lines and does not rate the usage again.

Quotes for these plans leave `included_units`, `billed_blocks`, `floor_uplift`,
and `ceiling_reduction` at 0. `usage_charge` equals `amount`.
