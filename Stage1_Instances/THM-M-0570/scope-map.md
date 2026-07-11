# Scope map

## Included subject boundary

- A closed smooth manifold and elliptic differential operator, or the graded Dirac-type operator
  selected by the eventual primary-source statement.
- Fredholm index, heat operators, trace or supertrace, and the small-time local heat-kernel
  asymptotics used to connect the analytic index to characteristic-class data.
- The analytic/topological index equality only when its exact bundles, symbols, orientations,
  coefficient conventions, and normalizations have been sourced.
- Boundary cases requiring later decisions include disconnected or zero-dimensional manifolds,
  real versus complex bundles, general elliptic versus Dirac-type operators, and manifolds with
  boundary (normally excluded from the classical closed-manifold statement).

## Required source decision

The metadata says only "heat-kernel proof of the index theorem" and glosses it as the Atiyah-Singer
theorem. That does not uniquely select among: (1) the McKean-Singer heat-trace identity for a
Z/2-graded elliptic complex; (2) the full cohomological Atiyah-Singer formula for a general elliptic
operator; (3) a Dirac-operator index formula such as the spin Dirac or Dolbeault case; or (4) a
local index theorem giving the pointwise small-time density. The statement phase must choose one
verbatim theorem from a stable primary source and preserve its hypotheses and normalization.

## Explicit exclusions

- Substituting finite-dimensional rank-nullity, Euler characteristic, or a toy matrix heat flow.
- Claiming the full index theorem from only the time-invariance of the heat supertrace.
- Using an assumed index equality or an abstract predicate as the conclusion-producing premise.
- Treating mathlib topology/manifold APIs or legacy metadata as a proof of the analytic theorem.

The later statement phase must freeze universes, manifold and bundle categories, ellipticity and
compactness hypotheses, operator domains, trace-class facts, characteristic-class conventions,
imports, declaration type, environment fingerprint, transports, and hypothesis mutations.
