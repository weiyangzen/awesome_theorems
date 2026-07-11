# Scope map

## Included root

Let `F` be the law of nonnegative interarrival times, let `mu` be its finite positive mean, and let
the renewal measure be

`U = sum_{n >= 0} F^{*n}`.

The root covers both standard branches of Blackwell's theorem:

- If `F` is nonarithmetic, then for every fixed `h > 0`, `U((x, x+h])` tends to `h / mu` as
  `x` tends to infinity.
- If `F` is arithmetic with maximal span `d > 0`, the renewal mass on a span-`d` lattice cell tends
  to `d / mu` along that lattice.

The branch distinction is semantic, not presentational. A proof of only the nonarithmetic branch or
only the arithmetic branch will not close this two-branch intake root.

## Statement-phase decisions

The next phase must inspect an exact source edition and decide the treatment of an atom at zero,
whether the law is carried by `[0, infinity)` or `(0, infinity)`, the definition of maximal arithmetic
span, the origin of the supporting lattice, the inclusion of the `n = 0` renewal, and open/closed
interval endpoints. It must also choose a precise filter formulation for `x -> infinity` and for the
lattice index, and prove transports between renewal-measure and cumulative-renewal-function forms.

The ordered binders, Borel measurability facts, integrability hypothesis, extended-real versus real
measure values, and minimal mathlib imports must follow those decisions. Boundary mutations must
include `mu = 0`, infinite mean, `h = 0`, a signed interarrival law, and use of a nonmaximal span.

## Explicit exclusions

- The elementary renewal theorem `U([0,x]) / x -> 1 / mu` by itself.
- Smith's key renewal theorem for a general directly Riemann integrable test function.
- A renewal-reward theorem, delayed-renewal theorem, or convergence-in-distribution statement.
- A finite-support, exponential, or deterministic interarrival special case substituted for the
  general result.
- The repository's untrusted `verified` metadata label as evidence of a human or machine proof.

No existing Lean declaration has been credited at intake. The formal target must use concrete
probability, convolution, measure, arithmeticity, and asymptotic-limit interfaces or record a precise
API blocker.
