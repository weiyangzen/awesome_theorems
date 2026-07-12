# THM-M-0167 rev-5.6 intake

This directory is the `planned` rev-5.6 instance for the repository target
named `辛格定理`. The local metadata attributes the result to James Simons in
1968 and describes it only as a rigidity theorem for minimal surfaces. That
evidence points toward the Simons minimal-submanifold theorem family, but it
does not identify one exact proposition. The Chinese title is also inconsistent
with the attribution: `辛格` normally transliterates Singer, whereas James
Simons and his results are normally rendered with a Simons transliteration.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Repository root | A rigidity or pinching result for minimal surfaces/submanifolds associated with James Simons (1968) | The repository does not state an inequality, ambient space, dimension, codimension, regularity, compactness, or equality case |
| Simons identity | A differential identity for the second fundamental form of a minimal submanifold | Possible proof ingredient or possible intended theorem; not selected as the root |
| Pinching/gap branch | Small second fundamental form forces a totally geodesic or otherwise rigid minimal submanifold | Candidate theorem family; the norm, threshold, and strict/equality cases remain open |
| Equality/classification branch | Clifford-type or other extremal examples in a sphere | Later refinements and classification results must not be folded into Simons's 1968 claim without a source-backed crosswalk |
| Geometric substrate | Minimal immersion/submanifold, induced metric, second fundamental form, curvature, and ambient Riemannian manifold | Concrete categories, universes, smoothness, connectedness, completeness, compactness, and boundary assumptions remain open |
| Name collision | I. M. Singer's local-homogeneity theorem for curvature-homogeneous Riemannian manifolds | Out of scope unless source audit disproves the James Simons/minimal-surface metadata |
| Formal system | Lean 4 and the repository's pinned mathlib environment | No declaration, target expression, minimal import, or proof artifact is claimed at intake |

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M4, R3]`. A primary
1968 Simons paper is identified as a discovery anchor, but its exact theorem,
assumptions, later corrections, and relation to the terse repository wording
have not been accepted. The first open theorem gate is exact-statement
identity. The statement phase must resolve the title/author mismatch and
select a source-pinned formula before freezing Lean binders or inspecting proof
closure. No machine proof, audit completion, or theorem completion is claimed.

## Validation

The exact intake checks and their results are recorded in `validation.md`.
They cover target membership, standard consistency, the pinned Lean toolchain,
JSON syntax, and dossier-local hygiene. Master acceptance remains outstanding.
