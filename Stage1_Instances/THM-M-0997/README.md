# THM-M-0997 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for Levy's spherical isoperimetric inequality. The
repository source supplies only the Chinese title, attribution/year, the phrase "isoperimetric
inequality for sets on the sphere," and an untrusted `verified` label. Intake therefore fixes the
neighbourhood-minimization form as the provisional exact human claim without granting source or
machine-proof credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | On a round sphere, a cap of equal normalized surface measure minimizes every geodesic neighbourhood measure | Primary edition/pinpoint and exact conventions remain open |
| Geometry | unit round `S^n`, geodesic distance, spherical caps | Lean representation, radius scaling, and dimension convention remain open |
| Measure | Borel-measurable sets and normalized Riemannian surface measure | Completion/measurability APIs and cap-existence witness remain open |
| Boundary cases | empty/full sets, `r = 0`, radii beyond the diameter, `n = 0` | Must be explicitly mutation-tested in the statement phase |
| Related forms | perimeter minimization and spherical concentration | No equivalence or consequence is credited; neither may replace the root |
| Exclusions | Euclidean/Gaussian isoperimetry, Poincare and log-Sobolev inequalities | Similar names and downstream consequences are not the assigned theorem |
| Foundations | Lean 4 kernel plus pinned mathlib and an accepted classical/measure/manifold profile | Toolchain, imports, dependency fingerprint, and axiom policy remain open |

The source-statement crosswalk records exactly what the local source does and does not establish.
The statement phase must either confirm the frozen neighbourhood form against a primary source or
revise the planned instance without claiming continuity of the statement fingerprint.

## Open task DAG

`INTAKE -> STATEMENT -> ANCHOR_AUDIT -> OBLIGATION_TREE -> PROOF -> VALIDATION -> RELEASE`

Only `INTAKE` is addressed here. Every dependent node remains open and is owned by its separately
accepted execution item.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H3, M4, R3]`. The first failed theorem gate is
source/statement identity: no primary-source edition and theorem/page pinpoint confirms the exact
variant, and no canonical Lean expression exists. The theorem is not complete.

## Validation

The exact intake-only checks, base revision, and results are recorded in `validation.md`. They show
manifest membership, standard consistency, JSON syntax, local reference integrity, and clean patch
format only. No Lean declaration or kernel evidence is claimed.
