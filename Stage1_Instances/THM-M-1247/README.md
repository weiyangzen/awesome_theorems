# THM-M-1247 rev-5.6 intake

This is a `planned` instance for the classical second-order, sharp-constant Rellich inequality. The
Chinese manifest label alone does not specify one of the several results called “Rellich inequality”;
this intake freezes the standard Euclidean `L2` form and excludes Rellich-Kondrachov compactness.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | `n >= 5`, real `u` smooth and compactly supported in `R^n \\ {0}` | Elaborated as `RellichInequalityTarget` in `Statement.lean` |
| Left side | Lebesgue integral of the squared Euclidean Laplacian | Laplacian is the standard-coordinate trace of the second Frechet derivative |
| Right side | weighted integral `|u(x)|^2 / ||x||^4` | The singularity is avoided by `0 ∉ tsupport u` |
| Constant | sharp squared constant `(n(n-4)/4)^2` over `Real` | Natural-number dimension is explicitly coerced before subtraction |
| Extensions | none | Sobolev completion, weighted variants, manifolds, and `Lp` analogues are excluded |
| Foundations | Lean 4.29.0 and pinned mathlib `8a178386...` | Statement uses three direct imports; proof-level trust remains open |

The likely architecture is a second-order integration-by-parts identity plus a sharp weighted
Cauchy-Schwarz/Hardy estimate, with density needed only for excluded extensions. This is an
orientation map, not a frozen obligation registry or proof credit.

## Statement verdict

Lifecycle remains `planned`; provisional root vector is `[H1, M3, R3]`. The exact statement, a
definitional expanded transport, environment fingerprint, minimal-import probes, and four structural
mutation fingerprints now elaborate against the pinned environment. This is statement/interface
evidence only. No proof or theorem-completion claim is made.

## Validation

Statement commands and results are recorded in `statement-validation.md`; intake checks remain in
`validation.md`. The generated blueprint and execution DAG were not edited.
