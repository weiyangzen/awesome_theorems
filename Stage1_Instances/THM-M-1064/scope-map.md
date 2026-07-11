# Scope map

## Frozen supplied scope

- The repository identifies the result as **Skorokhod embedding** and summarizes it as **embedding
  a random walk**.
- The subject is a stochastic process represented at stopping times of a driving process, with
  equality in distribution as the essential conclusion.
- The target formal system is Lean 4 with the repository's pinned mathlib dependency.

## Decisions required before statement acceptance

The statement phase must use an inspected primary source to choose exactly one root theorem:

1. the classical one-law Brownian embedding for a centered integrable real distribution;
2. the iterated stopping-time construction representing random-walk partial sums in Brownian
   motion; or
3. a genuinely sourced discrete-time/finite-state embedding theorem.

That source must determine the probability spaces, law and moment hypotheses, Brownian or discrete
driving process, filtration, stopping-time ordering and finiteness, equality-in-law granularity,
independence/conditional-law requirements, and any expectation or uniform-integrability conclusion.
It must also settle degenerate laws, zero variance, unbounded increments, and finite versus infinite
time horizons. Universes and binder order belong to the later exact Lean statement.

## Explicit exclusions

- Skorokhod's representation theorem for weak convergence, which is a different theorem.
- Merely defining a structure that contains the desired stopping times or law equalities as fields.
- Replacing the supplied random-walk claim by an easier finite-state exercise without a source
  crosswalk and checked transport.
- Treating optional stopping, hitting-time APIs, or stopped-value integrability alone as the
  terminal embedding theorem.

The historical `S1_M_220.lean` module is therefore discovery-only. Its variant selector and API
wrappers can inform later work but provide no rev-5.6 statement or proof credit.
