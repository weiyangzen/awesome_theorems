# Frozen obligation architecture

Item: `S56-M-1012-OBLIGATION_TREE`  
Registry version: 1  
Freeze date: `2026-07-12`

The registry freezes 14 root-relevant semantic obligations before the proof phase promotes any
candidate closure. The machine denominator has 12 required obligations; provenance and source are
informational for machine coverage but remain root-relevant release surfaces. Every obligation is
readability-eligible, and 11 carry human-source eligibility. The exact denominator digest is
`b62eb6e1869e2c7db9f45ad1ea1e5b467280a9a2fd75a339916b7c5a5815edfb`.

## M1012-root

The root is the exact elaborated known-limit equivalence from `Statement.lean`. It decomposes into
the forward and reverse implications. `root_of_directions` is a checked composition certificate
that consumes both exact child interfaces and returns the complete root.

## M1012-s-definitions

Freeze the weak topology on `ProbabilityMeasure E`, the measure coercions used by `charFun`, the
finite-dimensional real inner-product domain, universes, binders, and `atTop` convergence.

## M1012-s-boundaries

The architecture retains zero frequency, zero-dimensional `E`, constant or repeated sequences,
nonconvergent sequences, and both directions of the equivalence. It introduces no nondegeneracy
premise.

## M1012-s-foundation

The validation phase must accept the pinned import closure and the reported `propext`,
`Classical.choice`, and `Quot.sound` profile. No solver, oracle, or computational certificate is
part of the proof route.

## M1012-b-forward

Weak convergence supplies convergence of integrals of bounded continuous complex functions.
Instantiating this result with each inner-product characteristic function yields pointwise
characteristic-function convergence. This major imported branch remains a distinct obligation.

## M1012-b-reverse

Pointwise characteristic-function convergence must yield weak convergence. The checked
`reverse_of_tightness_and_separation` harness consumes both the tightness and weak-from-tight
children; neither may be hidden by the short upstream theorem invocation.

## M1012-c-tightness

Construct tightness of the sequence range from convergence to `charFun mu0`, using continuity of
the limiting characteristic function at zero.

## M1012-l-tight-analytic

Audit the analytic engine inside `isTightMeasureSet_of_tendsto_charFun`: the integral tail bound,
uniform domination, passage of the limit through the integral, continuity-at-zero estimate, and
conversion of those bounds into tightness. This is a critical semantic leaf with a 12-step budget,
not a primitive citation.

## M1012-l-weak-from-tight

Given tightness and characteristic-polynomial integral convergence, pass to compact subsequential
limits and use separation to identify every limit with `mu0`. This bridge includes the local/global
compactness transition and remains independently auditable.

## M1012-l-charpoly

Expand a characteristic polynomial as a finite sum and transport pointwise characteristic-function
convergence through scalar multiplication and finite sums to convergence of its integrals.

## M1012-l-separation

Verify that the characteristic-polynomial star subalgebra separates points via the real inner
product and `inner_self_ne_zero`.

## M1012-t-compose

Compose the two exact directional branches into the canonical `Iff`. The local Lean harness checks
the composition interface without supplying either child proof.

## M1012-x-provenance

Bind the local wrappers and graph nodes to the terminal mathlib body at revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, its source object and imported dependencies. This node
does not duplicate semantic proof credit.

## M1012-x-source

The exact primary-source edition, theorem/page, assumptions, normalization convention, errata, and
node-by-node crosswalk remain open. This is intentionally fail-closed at `H1`; the anchor audit did
not establish `H0`.

## Graph boundary

`typed-graphs.json` stores separate proof, refinement, provenance, evidence, trust, documentation,
and workflow graphs with reciprocal `proof_requires`/`composes` edges. The current root is open at
`M3`. No node has accepted evidence, and this phase claims neither proof acceptance nor theorem
completion.
