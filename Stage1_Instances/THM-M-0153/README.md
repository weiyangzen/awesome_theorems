# THM-M-0153 rev-5.6 intake

This directory is the `planned` intake dossier for the Chern-Gauss-Bonnet theorem catalogued under
differential geometry. The repository wording says that total curvature of a higher-dimensional
manifold is related to a characteristic number. This intake freezes the intended classical closed
even-dimensional formula: the integral of the normalized Pfaffian Euler form of the Levi-Civita
curvature equals the Euler characteristic.

## Scope map

| Surface | In scope | Intake boundary |
|---|---|---|
| Geometric domain | Compact, oriented, boundaryless Riemannian manifold of dimension `2n` | Precise Lean manifold model, universe, and binder order remain open |
| Differential-geometric side | Levi-Civita connection, curvature, normalized Pfaffian Euler form, oriented integral | Curvature sign, Pfaffian, and `(2 pi)` normalization must be pinned from an inspected source |
| Topological side | Euler characteristic of the same manifold | Concrete homology/cohomology or finite-complex representation remains open |
| Equality | Integral of the Euler form equals the Euler characteristic | Scalar codomain and coercions belong to the statement phase |
| Boundary behavior | Closed case; disconnected and zero-dimensional cases intended when conventions support them | Both require explicit statement probes; boundary correction formulas are excluded |
| Lean surface | Repository-pinned Lean 4 and mathlib | No exact declaration or expression is credited at intake |

The two-dimensional Gauss-Bonnet formula is a special case, not a substitute. An Euler-class
pairing theorem is not sufficient without a checked Chern-Weil bridge identifying its representative
with the normalized curvature Pfaffian. Noncompact, boundary, orbifold, and singular variants are
outside this target.

## Intake verdict

The provisional root vector is `[H1, M4, R4]`. Primary-source candidates are identified, but the
exact formula, assumptions, normalization, and errata have not received source review. No exact
Lean expression or proof body is claimed. The similarly named `THM-M-0569` is a separate catalog
target and only a discovery lead; its files and status provide no evidence credit here.

The open task DAG records every dependent rev-5.6 phase. Validation is limited to target-set
consistency, the pinned Lean executable, planned-instance invariants, JSON syntax, reference
integrity, and whitespace. Exact commands and results are in `validation.md`.
