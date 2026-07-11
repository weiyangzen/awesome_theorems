# Scope map

## Included claim

- A real-valued standard Wiener/Brownian process on a probability space, indexed by nonnegative
  real time and starting at zero.
- Almost-sure continuity of sample paths (or of the canonical continuous modification, according
  to the selected source's definition of Wiener process).
- Almost-sure nowhere differentiability at every time in the nonnegative-time domain, using the
  appropriate one-sided/domain-relative meaning at zero.

## Decisions reserved for statement freeze

The inspected primary source must decide whether continuity is definitional or a conclusion,
whether the result concerns a given process or an indistinguishable/coordinatewise-a.e.
modification, whether the two almost-sure properties share one full-measure event, and the precise
notion of differentiability at the endpoint. The statement phase must also freeze probability
measure assumptions, completion/measurability conventions, time representation (`ℝ≥0`, a subtype,
or `Set.Ici 0`), binder order, and universes.

## Explicit exclusions

- Merely proving continuity without nowhere differentiability, or nowhere differentiability of a
  generic continuous function.
- A discrete random walk, fractional Brownian motion, multidimensional Brownian motion, or a
  deterministic surrogate in place of the real standard Wiener process.
- Assuming continuity or nowhere differentiability as fields of a conclusion package and then
  projecting them.
- Kolmogorov moment bounds alone, which are at most an input to continuity and do not establish the
  full source theorem.

The later formal target must connect a concrete Brownian-law predicate to both path conclusions or
record a precise API/integration blocker.
