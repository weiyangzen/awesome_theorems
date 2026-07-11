# Scope map

## Included claim

- Time is nonnegative real time and the state space is real-valued.
- The process is adapted to a filtration on a probability space, has continuous sample paths, and
  starts at zero (with the source's precise almost-sure convention still to be fixed).
- Both `X` and `t |-> X_t^2 - t` are martingales relative to the same filtration.
- The conclusion is that `X` is a standard Brownian motion relative to that filtration, including
  the appropriate Gaussian increment laws and independence from the past.

## Statement-phase decisions

The selected primary edition must fix the usual conditions on the filtration, whether continuity
and the initial value hold pointwise or almost surely, and the exact integrability implicit in
"martingale." It must also decide whether the conclusion is expressed by conditional
characteristic functions, increments independent of `F_s`, or a Brownian-motion predicate. Binder
order, universes, measurability, and probability-measure assumptions must then be frozen in Lean.

## Explicit exclusions

- The converse direction (that Brownian motion has these martingales) as a substitute.
- A discrete-time, finite-state, stopped, local-martingale, multidimensional, or merely Gaussian
  special case.
- Assuming independent Gaussian increments or Brownian motion in an input structure.
- Treating an abstract conclusion package with its desired fields as a proof.
- Treating the legacy `S1_M_222.lean` statement boundary or helper lemmas as terminal closure.

Degenerate probes for the statement phase include the zero process, non-probability measures,
non-usual filtrations, and weakening either martingale hypothesis. They are tests of statement
identity, not alternate targets.
