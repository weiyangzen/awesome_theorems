# Scope map

## Included claim

- A real-valued standard Brownian motion starting at zero, on a filtered probability space with
  the usual measurability and path-continuity conditions required by the selected source.
- A random field `L(t,a)` indexed by nonnegative time `t` and spatial level `a : R` that is a
  jointly continuous version of Brownian local time.
- The occupation-density identity, almost surely, simultaneously in time and for the test-function
  class fixed by the selected source. The intended normalization is
  `integral_0^t f(B_s) ds = integral_R f(a) L(t,a) da`.
- The properties needed to make this an existence theorem rather than a definition: nonnegativity,
  appropriate measurability, and support at levels visited by the path, when these are included in
  the selected theorem or required to characterize its local-time version.

## Statement-phase decisions

The selected source must determine whether time ranges over `[0,T]` or all nonnegative reals; the
filtration assumptions; the exceptional null set and the order of the `almost surely`, `for every
t`, and `for every f` quantifiers; the precise test-function class; and whether joint continuity is
part of the same theorem or a companion result. It must also fix endpoint conventions and the
factor-of-two normalization used when local time is instead defined through Tanaka's formula or
quadratic-variation occupation density. Binder order and universes must follow those decisions.

## Explicit exclusions

- Tanaka's formula alone, without constructing and identifying the occupation density.
- A local time for one fixed level only, or an equality for one fixed test function only, as a
  substitute for the jointly continuous field and its quantified occupation formula.
- Local time for a general semimartingale or diffusion unless specialized and transported to the
  exact Brownian claim.
- Discrete random-walk visit counts, multidimensional intersection local time, boundary local time,
  or a deterministic path occupation measure.
- A structure or hypothesis that assumes the desired local-time field and occupation identity.

The later formal target must connect an actual Brownian process, Lebesgue time and space integrals,
the probability-one event, and joint continuity, or record a precise missing-API blocker.
