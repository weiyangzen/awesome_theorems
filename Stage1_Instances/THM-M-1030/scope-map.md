# Scope map

## Included claim

- A filtered probability space and a real-valued, continuous local martingale `M` with `M 0 = 0`.
- Its continuous quadratic variation (bracket) process `⟨M⟩` and the generalized inverse
  `T s = inf {t | ⟨M⟩ t > s}` (with the exact inequality and endpoint convention source-frozen later).
- Under almost-sure divergence of the bracket, `B s = M (T s)` is a standard Brownian motion and
  `M t = B (⟨M⟩ t)` almost surely.
- The theorem's filtration and probability-space extension clauses, if required by the selected
  primary formulation.

## Statement-phase decisions

The exact source must decide whether the result begins with a continuous local martingale or a
continuous martingale, whether divergence of the bracket is assumed, and whether equality is
indistinguishability, per-time almost-sure equality, or pathwise outside one null set. It must also
freeze completed/right-continuous filtration hypotheses, the definition of quadratic variation,
the `>` versus `>=` inverse convention, measurability/stopping-time claims, and behavior when the
bracket has finite terminal value. Domains (`ℝ≥0`, `ℝ`, or extended time), binder order, universes,
and Brownian motion's filtration must follow those decisions.

## Explicit exclusions

- Levy's characterization, the martingale representation theorem, or a discrete-time embedding as
  a substitute for the continuous time-change theorem.
- Merely proving Gaussian marginals, independent increments, or a deterministic time-change case.
- Treating quadratic variation, inverse-time correctness, or Brownian motion as unconstrained
  proposition fields supplied by the caller.
- Crediting the legacy `S1_M_223.lean` `StatementShape`: several essential stochastic-analysis
  facts are stored as opaque `Prop` fields and its terminal implication has no proof.

The formal target remains open until concrete stochastic-process APIs express every included
notion and checked transports connect any alternate encoding to the source-frozen statement.
