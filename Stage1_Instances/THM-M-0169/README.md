# THM-M-0169 rev-5.6 intake

This directory is the `planned` rev-5.6 instance for Hilbert's theorem on complete surfaces of
constant negative Gaussian curvature. The manifest's Chinese source wording is: "A complete
surface of constant negative curvature cannot be isometrically immersed in R^3." Intake does not
inherit proof credit from the source label `已验证` and does not claim a Lean statement or proof.

## Scope map

| Surface | In scope | Intake boundary |
|---|---|---|
| Root | Nonexistence of a global isometric immersion into Euclidean three-space | Exact regularity and source-equivalence remain open |
| Domain | A complete two-dimensional Riemannian manifold | Connectedness, boundarylessness, second countability, and the precise completeness notion require statement/source audit |
| Geometry | Constant Gaussian curvature `-1` and pullback equality with the Euclidean metric | An arbitrary constant `K < 0` is only a scaling candidate |
| Map | A sufficiently regular immersion `f : M -> R^3` | The minimum differentiability needed for curvature and the theorem is not frozen |
| Primary-source form | Hilbert's everywhere regular analytic surface with his global finite-accumulation condition | No unproved equivalence to modern metric completeness is credited |
| Proof architecture | Asymptotic coordinates, global topology, finite total area, infinite disk area, contradiction | Architecture is a scope forecast, not a frozen obligation registry |
| Formalization | Lean 4 plus pinned mathlib | No declaration, expression fingerprint, environment fingerprint, or machine anchor exists at intake |

The target must not be broadened to Efimov's variable-curvature theorem, weakened to a local
surface claim, or replaced by a theorem about embeddings. Local pseudospherical patches and
incomplete immersed surfaces are boundary cases rather than counterexamples to the scoped root.

## Source boundary

Hilbert's primary paper is identified precisely in `source_statement_crosswalk.md`. Its conclusion
on printed pp. 96-97 rejects an everywhere regular analytic surface of constant negative curvature
and the realization of the whole Lobachevskian plane. The repository wording is a standard modern
reformulation, but the bridge between Hilbert's hypotheses and the proposed complete-Riemannian-
manifold formulation is not established here. Consequently the human axis remains `H1`.

## Open execution DAG

`task-dag.json` records the dependent rev-5.6 phases and the intake subtasks. Every task remains
`open`; only the integration lane can accept this worker's intake receipt. The next hard gate is
source-faithful selection of regularity and completeness, followed by elaboration of an exact Lean
proposition with minimal pinned imports.

## Status

Lifecycle is `planned`; root vector is `[H1, M4, R3]`; `theorem_complete` is false. Structural
self-validation checks membership, exact dossier identities, JSON shape, open-state invariants,
and local path references. It is not kernel evidence and does not discharge the statement phase.
