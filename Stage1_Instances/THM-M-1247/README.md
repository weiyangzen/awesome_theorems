# THM-M-1247 rev-5.6 intake

This is a `planned` instance for the classical second-order, sharp-constant Rellich inequality. The
Chinese manifest label alone does not specify one of the several results called “Rellich inequality”;
this intake freezes the standard Euclidean `L2` form and excludes Rellich-Kondrachov compactness.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | `n >= 5`, real `u` smooth and compactly supported in `R^n \\ {0}` | A Lean expression and normalized hash belong to the statement phase |
| Left side | Lebesgue integral of the squared Euclidean Laplacian | Laplacian convention and measurability/integrability APIs require elaboration |
| Right side | weighted integral `|u(x)|^2 / ||x||^4` | The singularity is avoided by the support hypothesis |
| Constant | sharp squared constant `(n(n-4)/4)^2` over `Real` | Coercions and algebraic normalization are not yet checked |
| Extensions | none | Sobolev completion, weighted variants, manifolds, and `Lp` analogues are excluded |
| Foundations | Lean 4 kernel and pinned mathlib | Exact toolchain, imports, axioms, and TCB remain open |

The likely architecture is a second-order integration-by-parts identity plus a sharp weighted
Cauchy-Schwarz/Hardy estimate, with density needed only for excluded extensions. This is an
orientation map, not a frozen obligation registry or proof credit.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M4, R3]`. The first failed theorem gate is
the exact Lean statement gate: no declaration, elaborated expression, environment fingerprint,
transport, or mutation evidence exists. The theorem is not complete.

## Validation

The exact commands and results establishing manifest membership, standard consistency, JSON syntax,
and dossier-local reference integrity are recorded in `validation.md`. The pre-existing modifications
to the generated blueprint and execution DAG were observed and were not edited by this intake.
