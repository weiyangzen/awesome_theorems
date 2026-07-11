# Scope map

## Included claim

- A discrete-time real-valued martingale `f n` on a probability space with a filtration.
- Two stopping times `tau` and `pi`, ordered pointwise by `tau <= pi`.
- A deterministic natural-number bound on `pi`, hence also on `tau`.
- Equality of the integrals (expectations) of `stoppedValue f tau` and `stoppedValue f pi`.

## Statement-phase decisions

The primary source must confirm whether both stopping times must be bounded or whether boundedness
of the later time plus the ordering is the stated convention. The statement phase must also freeze
almost-everywhere versus pointwise ordering, integrability hypotheses, the filtration's sigma-finite
interface, treatment of `WithTop` infinity, binder order, universes, and equality in `Real` rather
than an extended expectation type.

## Explicit exclusions

- Optional sampling inequalities for submartingales as a substitute for martingale equality.
- Unbounded stopping-time variants based on uniform integrability or dominated convergence.
- Continuous-time martingales, stochastic integrals, or Brownian-motion-only special cases.
- Deterministic-time expectation constancy alone.
- A structure that assumes the desired equality as a field.

The initial formal candidate is the legacy `StatementShape` in
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_284.lean`. It is not accepted by this intake and
must be independently elaborated, source-matched, mutation-tested, and audited downstream.
