# Scope map

## Included claim

- A triangular array of real random variables, with independence within each finite row.
- Centering by each entry's expectation and scaling by the square root of the sum of row variances.
- A fixed real `delta > 0` and finite absolute centered moments of order `2 + delta`.
- The Lyapunov ratio tending to zero as the row index tends to infinity.
- Weak convergence in distribution of normalized row sums to the standard Gaussian law.

## Statement-phase decisions

The canonical Lean target uses the first `n` entries of row `n` on one probability space. It centers
each entry explicitly, assumes eventual strict positivity of the summed row variance, requires
measurability, finite second moments, and integrability of every centered `2 + delta` moment, and
concludes mathlib weak convergence in distribution. The target quantifies universe-polymorphically
over separate source and Gaussian realization spaces. Degenerate rows are allowed only outside an
eventual tail. These encoding choices implement the frozen human scope but remain subject to the
later pinpoint source audit; they are not inherited from the legacy bridge-bearing structure.

## Explicit exclusions

- The identically distributed CLT, Lindeberg-Feller CLT, or Berry-Esseen bound as a substitute.
- Pairwise independence in place of the source theorem's joint row independence.
- A finite or discrete special case presented as the full theorem.
- Assuming characteristic-function convergence, a Taylor bridge, or the desired weak convergence
  as structure data.
- The wrappers and boundary metadata in `S1_M_270.lean` as terminal proof evidence.

The statement phase must produce a concrete mathlib expression and checked boundary cases; until
then the human scope is frozen but the formal target remains open.
