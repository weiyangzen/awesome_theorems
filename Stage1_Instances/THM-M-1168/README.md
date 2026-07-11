# THM-M-1168 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the catalog claim "interior
estimates" (`内部估计`). It inherits no proof credit from the Stage0 label
`已验证`.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Catalog root | Interior regularity of solutions | The catalog does not name an equation, solution concept, domain, coefficient class, norms, derivative order, or estimate |
| Candidate PDE families | Elliptic, parabolic, and other interior estimates | Candidates are alternatives, not interchangeable formulations |
| Local geometry | A subdomain compactly contained in the equation domain, or nested balls/cylinders | Exact geometry and distance-to-boundary dependence remain open |
| Analytic data | Operator, forcing term, coefficients, and their regularity/ellipticity assumptions | No assumptions may be selected merely to obtain a convenient theorem |
| Conclusion | A quantitative interior estimate implying a specified regularity gain | Neither the source nor destination function spaces are frozen |
| Foundations | Lean 4 kernel plus pinned mathlib | Toolchain, imports, classical axioms, and dependency closure remain open |

The intended theorem family cannot yet be narrowed without changing the human
claim. In particular, a harmonic-function estimate, a Schauder estimate, and an
interior `W^{2,p}` estimate have materially different hypotheses and conclusions.
The dependent statement phase must first resolve that source ambiguity from an
authoritative source; it must not silently choose one of these variants.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H4, M4, R3]`. The first
failed gate is source identification: the inherited phrase is not an exact
theorem statement. Consequently there is no canonical Lean expression, no
elaboration fingerprint, and no proof claim. The theorem is not complete.

## Validation

The exact intake checks and results are recorded in `validation.md`. They
establish target membership, repository-standard consistency, JSON syntax, and
dossier-local integrity only.
