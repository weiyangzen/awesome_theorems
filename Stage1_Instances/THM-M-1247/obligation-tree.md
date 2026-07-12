# THM-M-1247 obligation architecture

The frozen proof route is the classical weighted integration-by-parts and
Hardy-estimate route. It is an architecture, not a proof claim. The exact root
remains `M3`; every substantive analytic leaf remains open at `M4`.

## M1247-ROOT
The exact proposition in `Statement.lean` is the only root.

## M1247-S-LAPLACIAN
Relate the coordinate trace definition to the Laplacian occurring in the
weighted identities. No mathlib operator theorem is credited as the estimate.

## M1247-S-DOMAIN
Propagate smoothness, compact support, and avoidance of zero so all weights,
derivatives, and boundary-free integrations are justified.

## M1247-S-BOUNDARY
Cover `n >= 5`, the zero function, behavior near zero, measurability, and
integrability. Dimension four is not silently admitted.

## M1247-S-FOUNDATION
Audit the Lean kernel and the classical/quotient/integration primitives.

## M1247-N-WEIGHTS
Normalize norm powers and prove the algebra of the sharp coefficient
`(n * (n - 4) / 4)^2` without division or extended-integral ambiguity.

## M1247-L-IBP
Establish every weighted multidimensional integration-by-parts identity and
its vanishing boundary term.

## M1247-L-HARDY
Establish the sharp weighted first-derivative Hardy estimate required by the
selected proof route.

## M1247-L-CORE
Combine `IBP`, `HARDY`, `WEIGHTS`, and the domain/boundary packages to produce
`CoreRellichEstimate`, definitionally the fully expanded target.

## M1247-T-TRANSPORT
`root_of_coreRellichEstimate` is a checked conditional transport through the
statement-phase equivalence. It gives no proof credit to the open premise.

## M1247-X-SOURCE
A pinpoint complete human-source proof remains required; the intake crosswalk
is not yet H0 evidence.

## M1247-X-PROVENANCE
Terminal proof bodies must be recorded and deduplicated from wrappers.

## M1247-X-TRUST
Imports, axioms, and reproducible command evidence remain release obligations.

The proof graph is `ROOT -> T-TRANSPORT -> L-CORE`, with six required children
of `L-CORE`: `L-IBP`, `L-HARDY`, `N-WEIGHTS`, `S-BOUNDARY`, `S-DOMAIN`, and
`S-LAPLACIAN`. Source, provenance, trust, documentation, and workflow edges
are segregated and cannot close a proof node.
