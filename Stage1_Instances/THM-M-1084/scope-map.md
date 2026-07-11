# Scope map

## Included claim

- A real-valued, centered, separable Gaussian process `(X_t)_{t in T}` on a nonempty index type.
- The canonical increment pseudometric
  `d(s,t) = sqrt(E[(X_s - X_t)^2])`; no unrelated externally supplied metric may replace it without
  a checked domination bridge.
- Metric covering numbers `N(T,d,epsilon)` and the entropy integral
  `integral_0^diam sqrt(log N(T,d,epsilon)) d epsilon`.
- Under total boundedness and finiteness of that integral, a universal-constant upper bound on
  `E[sup_t (X_t - X_t0)]` for a fixed base point `t0`.
- The singleton boundary case: the increment supremum and entropy integral must both reduce to zero.

## Statement-phase decisions

The statement phase must select and inspect one exact source formulation before choosing the
universal constant and the upper integration limit. It must fix the definition of covering number
for a pseudometric quotient, open versus closed balls, extended-real conventions, and the meaning
of the integral at zero. It must also fix separability/measurability assumptions that make the
uncountable supremum a measurable integrable random variable, and decide whether the result is
encoded directly for Gaussian processes or through a checked Gaussian-to-sub-Gaussian increment
bridge. Binder order, universes, probability-space hypotheses, and all finiteness side conditions
must be explicit in the canonical Lean target.

## Explicit exclusions

- A finite-index chaining inequality presented as the full separable-process theorem without a
  checked limiting argument.
- A bound for `E[sup_t X_t]` without centering, a base point, or an equivalent checked transport.
- An arbitrary sub-Gaussian process as a silent replacement for the named Gaussian theorem. A
  stronger sub-Gaussian theorem is usable only with an exact checked specialization.
- Only a sample-continuity criterion, almost-sure boundedness result, Borell-TIS concentration
  inequality, Sudakov lower bound, or generic-chaining comparison.
- Defining covering numbers or assuming the desired entropy bound as a field of a structure.

The canonical claim permits different conventional numerical constants only until the exact source
is selected. The statement phase must freeze one normalization; later proof work may not change it
to fit an available library theorem.
