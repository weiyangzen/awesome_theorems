# Scope map

## Included claim

- A finite indexed family of real random variables on one probability space.
- Independence, measurability/integrability as required to define expectation, and almost-sure bounds
  `a i <= X i <= b i`.
- The one-sided upper tail of the centered sum for every nonnegative real threshold `epsilon`.
- The sharp Hoeffding exponent `-2 * epsilon^2 / sum i, (b i - a i)^2`, or a definitionally or
  algebraically checked equivalent variance-proxy form.

## Statement-phase decisions

Freeze the finite index representation, binder order, probability-measure typeclass placement,
event measurability, and expectation notation. Check the empty family, `epsilon = 0`, and zero total
range explicitly; division-by-zero behavior must not silently change the mathematical boundary
case. Decide whether bounds are pointwise or almost sure according to the source-to-Lean transport.

## Explicit exclusions

- A two-sided absolute-value estimate unless derived as an additional corollary.
- Identically distributed variables, equal-width intervals, martingale differences, or bounded
  differences of a general function as substitutes for the independent bounded-variable theorem.
- Bernstein, Bennett, Azuma-Hoeffding, or McDiarmid inequalities.
- Treating the legacy wrapper or an upstream theorem name as accepted proof evidence.

The legacy `S1_M_274.lean` centered initial-segment formulation is a candidate encoding, not the
frozen rev-5.6 statement. Its equivalence to the source exponent and all degenerate cases remain
statement-node obligations.
