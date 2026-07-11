# THM-M-0166 frozen obligation architecture

Item `S56-M-0166-OBLIGATION_TREE` freezes registry version 1 before proof execution. The seven
canonical nodes and their eligibility denominators are authoritative in `obligation-registry.json`
and `typed-graphs.json`. No node is excluded because it is hard or currently open.

## Root

`M0166-ROOT` is the exact statement fingerprint `8965e82e...a55`. Its checked Lean composition
consumes `M0166-L-EXISTENCE` and `M0166-L-SUBSEGMENT`. Both are typed propositions, not asserted
theorems, so the root remains `M2` and theorem completion is false.

## Statement interface

`M0166-S-INTERFACE` retains the explicit universes, finite dimension, boundaryless smooth
Riemannian structure, connectedness, metric completeness, all endpoint pairs, and all ordered
subsegments. Alternate properness and exponential-map forms are not silently substituted.

## Distance substrate

`M0166-X-DISTANCE` owns the pinned mathlib lower-bound and arbitrarily-short-path declarations.
They establish approximation to `riemannianEDist`, not attainment of its infimum.

## Properness package

`M0166-C-PROPER` is the critical open local-to-global bridge: derive the compact control needed for
minimizer extraction from finite-dimensional Riemannian local structure and completeness. The
pinned `complete_of_proper` declaration has the reverse direction and does not close this node.

## Global minimizer

`M0166-L-EXISTENCE` must construct, for arbitrary endpoints, a smooth path whose total length is
their Riemannian distance. Its ledger exposes approximation, compact confinement, convergence,
endpoint preservation, lower semicontinuity, and regularity as separate proof work.

## Subsegment minimality

`M0166-L-SUBSEGMENT` converts global endpoint minimality into every-subsegment minimality. Its
future proof must model restriction, competitor concatenation, smoothness, reparameterization, and
length additivity. These are not hidden behind the root composition.

## Trust boundary

`M0166-X-TRUST` owns eventual terminal dependency, axiom, computation, and TCB classification.
There is no computation boundary in the frozen plan. Release-grade trust closure remains pending.

## Workflow and boundary

The workflow graph records anchor audit -> obligation tree -> proof -> validation -> release.
The current minimal open root cut set is `M0166-C-PROPER`, `M0166-L-EXISTENCE`, and
`M0166-L-SUBSEGMENT`. This architecture is provisional pending master acceptance and supplies no
proof, source-review, readability-review, hermetic-validation, or theorem-completion credit.
