# THM-M-1129 rev-5.6 intake

This directory is the `planned` dossier for Poisson's formula for the Cauchy problem for the
two-dimensional wave equation. The Stage0 description, "solution of the two-dimensional wave
equation," is not precise enough to be a formal statement, so this intake does not silently choose
regularity assumptions or claim exact-statement closure.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| PDE root | `u_tt = c^2 Delta u` on `R^2`, `c > 0`, with displacement `f` and velocity `g` | Function spaces and uniqueness class remain open |
| Representation | time derivative of the weighted disk integral of `f`, plus the corresponding integral of `g` | Kernel normalization must be checked against a pinned source |
| Geometry | disks centered at `x` of radius `c*t`; equivalently a unit-disk change of variables | No transport is credited yet |
| Boundary | recovery of `f` and `g` as `t -> 0+` | Direct substitution at `t=0` is excluded because the displayed kernel is singular |
| Analysis | differentiation under the integral, Laplacian/time derivative identity, integrability near the disk boundary | All are future typed obligations |
| Exclusions | bounded domains, forcing terms, nonlinear equations, weak/distributional-only solutions | These would be different theorems |
| Foundations | Lean 4 kernel, pinned mathlib analysis and measure APIs | Imports, toolchain, axioms, and dependency closure remain open |

The statement phase must select a source-faithful regularity theorem rather than broaden the vague
Stage0 label. It must freeze ordered binders, the exact disk convention (`<` versus `<=`, irrelevant
only after a checked boundary-null argument), constants, derivatives, and uniqueness conclusion.

## Open task DAG

`INTAKE -> STATEMENT -> ANCHOR_AUDIT -> OBLIGATION_TREE -> PROOF -> VALIDATION -> RELEASE`.
The dependent statement task must elaborate the exact target and mutation-test `c > 0`, `t > 0`,
dimension two, both initial conditions, kernel exponent, and normalization. Later audit work must pin
primary sources and search mathlib without treating a PDE API fragment as closure.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M4, R3]`. The first failed theorem gate is
the exact statement gate: no fully specified source statement, Lean declaration, elaborated hash, or
environment fingerprint exists. The theorem is not complete.

## Validation

The commands and results in `validation.md` establish manifest membership, repository-standard
consistency, JSON syntax, and dossier-local integrity only.
