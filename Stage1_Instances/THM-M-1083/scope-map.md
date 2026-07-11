# Scope map

## Included root

- A real-valued stochastic process indexed by the compact interval `[0,T]`, with `T > 0`, on a
  probability space.
- Positive real exponents `alpha` and `beta`, a nonnegative constant `C`, and the uniform increment
  estimate `E[|X_t-X_s|^alpha] <= C |t-s|^(1+beta)` for all `s,t` in the interval.
- Existence of one modification `Y`: for every fixed `t`, `X_t = Y_t` almost surely.
- For each `gamma` strictly between zero and `beta/alpha`, almost every sample path of `Y` has a
  finite `gamma`-Holder seminorm on the compact interval. Continuity is a consequence, not a
  replacement for the stronger frozen conclusion.

## Statement-phase decisions

The next phase must select the exact mathlib representations of the probability space, process,
expectation, real powers, interval subtype, modification relation, and Holder predicate. It must
also decide whether path measurability is derived or stated, how null sets depend on `gamma`, and
whether the conclusion is encoded by a seminorm, `HolderWith`, or an equivalent predicate. Binder
order, namespaces, minimal imports, normalized expression hash, and environment fingerprint remain
open.

Boundary probes must cover `T = 0`, `C = 0`, coincident times, `alpha <= 0`, `beta <= 0`, and the
excluded endpoint `gamma = beta/alpha`. Removed measurability or moment assumptions, a changed time
domain, and swapping fixed-time almost-sure equality with a single simultaneous null set are
nontrivial mutations requiring explicit checks.

## Explicit exclusions

- A process already assumed to possess the requested continuous or Holder modification.
- A result that provides only stochastic continuity, continuity in probability, or continuity of
  the mean.
- A result that proves the moment condition but does not construct a modification.
- A Brownian-motion-only corollary in place of the general increment criterion.
- The critical Holder exponent `gamma = beta/alpha`.
- A multiparameter or metric-valued generalization silently substituted for this root; such a
  theorem may later be used only with checked specialization.
- A mere definition or record packaging the desired conclusion.

## Current boundary

This map freezes the human mathematical target, not its Lean expression. No legacy module or
mathlib declaration has been accepted. The source, statement, anchor, obligation-tree, proof,
validation, and release gates remain independent downstream work.
