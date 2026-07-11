# Scope map

## Included claim

- A real Banach space `X` and a continuously Frechet-differentiable functional `Phi : X -> R`.
- Palais-Smale compactness: bounded functional values and derivative tending to zero yield a
  convergent subsequence (with the precise sequential formulation deferred to source inspection).
- Mountain-pass geometry based at `0`: a positive barrier on a sphere of radius `rho`, and an
  endpoint `e` outside that sphere whose value is no greater than the base value.
- The path minimax `c = inf {max Phi(path t)}` over continuous paths joining `0` to `e`.
- Existence of a critical point at level `c`, with `c` at least the barrier level.

## Statement-phase decisions

The inspected primary text must settle whether `Phi(0) = 0` is normalized or only used relative to
the barrier, whether the endpoint inequality is strict, the exact Palais-Smale formulation, and
whether the conclusion explicitly supplies a point `x` with `Phi x = c` and derivative zero.
Binder order, derivative representation, topology on the path space, and the treatment of empty or
degenerate path families must follow those choices.

## Explicit exclusions

- The finite-dimensional mountain pass lemma without a Palais-Smale hypothesis as a substitute.
- A deformation lemma, minimax principle, saddle-point theorem, or PDE application alone.
- Assuming the desired critical point or critical value inside an abstract package.
- Weakening the conclusion to an approximate critical sequence.

The later formal statement must use concrete normed-space, Frechet derivative, compactness, path,
and infimum interfaces, or record a precise missing-API blocker.
