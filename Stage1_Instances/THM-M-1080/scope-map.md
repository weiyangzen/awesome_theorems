# Scope map

## Included claim

- A probability space with a discrete filtration and a finite real-valued martingale
  `X_0, ..., X_n` adapted to it.
- Deterministic bounds `c_k >= 0` with `|X_k - X_{k-1}| <= c_k` almost surely for every
  `k = 1, ..., n`.
- For every real `t >= 0`, the upper tail
  `P(X_n - X_0 >= t) <= exp(-t^2 / (2 * sum c_k^2))`.
- The lower-tail result obtained by applying the same theorem to `-X`, and the two-sided result
  obtained by a union bound, are named downstream transports.

## Statement-phase decisions

The exact source transcription must decide whether the root uses a martingale, martingale
differences with zero conditional expectation, or predictable interval bounds. It must also freeze:

- finite indices (`Fin (n+1)`, an interval of naturals, or a finite set) and binder order;
- the filtration and adaptedness API, integrability, and conditional-expectation equality;
- whether increment bounds are pointwise or almost everywhere and how all-time exceptional sets are
  combined;
- the probability event syntax and extended-real-to-real comparison;
- the `n = 0`, `t = 0`, and `sum c_k^2 = 0` cases, avoiding division by zero;
- constants in the exponent, especially the distinction between absolute bounds `c_k` and interval
  widths `b_k-a_k`.

## Explicit exclusions

- Independent-variable Hoeffding concentration with no martingale filtration.
- A bound for only identically bounded increments when the intended statement permits varying
  deterministic bounds.
- A variance-sensitive Freedman or Bernstein inequality in place of Azuma's bounded-difference
  estimate.
- A submartingale maximal inequality, asymptotic convergence claim, or expectation bound alone.
- Assuming the exponential supermartingale or the desired tail inequality as a hypothesis.
- Substituting only the lower-tail or two-sided corollary without checked transport to the selected
  canonical direction.

## Formalization boundary

No Lean module or declaration is selected at intake. Later phases must either integrate an exact
pinned theorem through a checked wrapper or implement the required exponential-moment argument.
Any mismatch in constants, event direction, time indexing, almost-sure scope, or hypotheses remains
statement or integration debt rather than proof credit.
