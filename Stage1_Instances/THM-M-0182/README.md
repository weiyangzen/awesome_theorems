# THM-M-0182 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for Perelman's geometrization theorem and its
Poincare-conjecture corollary. The manifest's historical `verified` source label is untrusted and
supplies no Lean proof credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact human root | Thurston geometrization for closed, connected, orientable 3-manifolds | A precise formal decomposition/geometric-structure predicate is not yet available |
| Named corollary | A closed simply connected 3-manifold is homeomorphic to `S^3` | Strictly a corollary, not a substitute for the geometrization root |
| Topological layer | 3-manifolds, prime/JSJ decomposition, incompressible tori, homeomorphism | Exact categories and existing mathlib APIs require statement-phase audit |
| Geometric layer | The eight model geometries and finite-volume geometric pieces | Metrics, group actions, quotients, and completeness must be explicitly encoded |
| Analytic architecture | Ricci flow, singularity control, surgery, noncollapsing, extinction | Architecture only; no analytic lemma or closure is claimed |
| Foundations | Lean 4 kernel plus pinned topology, manifold, and analysis dependencies | Toolchain, imports, axioms, and environment fingerprint remain open |

The full geometrization conclusion is the root because the legacy blueprint says both geometrization
and Poincare were proved. Recording only the much narrower Poincare corollary would broaden the
completion claim by silently dropping most of the assigned theorem. Conversely, the Ricci-flow
papers provide proof machinery, not an alternate statement.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M4, R3]`. The first failed theorem gate is
the exact statement gate: there is no canonical Lean declaration, elaborated expression hash,
environment fingerprint, or checked transport. The theorem is not complete. Structured scope is in
`intake.json`, source relationships are in `source_statement_crosswalk.md`, and the narrow validation
record is in `validation.md`.
