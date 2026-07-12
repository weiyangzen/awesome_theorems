# Exact-statement gate: blocked

Item: `S56-M-0584-STATEMENT`  
Theorem: `THM-M-0584`  
Base revision: `7f7539be2690c4075e12d47f531aae8b181f4944`

## Decision

The exact Lean 4 target cannot be truthfully selected or elaborated from the authoritative material.
The repository supplies only "Donaldson theorem" and "differential structures of four-dimensional
manifolds." The intake dependency interprets this provisionally as Donaldson's diagonalization
theorem, but explicitly leaves primary-source theorem/page identity and the exact claim open.

Those omissions change the proposition. The dossier has not accepted whether the root is stated for
positive-definite forms only or for definite forms via orientation reversal; the precise closedness,
connectedness, boundary, and orientation conventions; the carrier of the integral intersection form
and its torsion quotient; or whether diagonalization is expressed by a basis, a lattice isometry, or
a matrix congruence. Even the identification of this theorem family, rather than another result
about four-manifold smooth structures, still requires independent source acceptance. Selecting the
familiar modern formulation would therefore invent missing mathematics and violate the exact-source
identity gate.

Consequently no ordered binders, canonical Lean expression, expression hash, alternate-form
transport, or meaningful removed-hypothesis/domain/binder-scope/boundary mutations can be frozen.
An opaque intersection-form parameter or a hypothesis containing the desired diagonalization would
assume away the geometric content and is not an allowed substitute.

## Pinned Lean boundary

`StatementInfrastructure.lean` checks the nearest independent substrates available in the pinned
environment using three direct imports:

```lean
import Mathlib.AlgebraicTopology.SingularHomology.Basic
import Mathlib.Geometry.Manifold.Bordism
import Mathlib.LinearAlgebra.BilinearForm.Properties
```

Pinned mathlib exposes closed smooth-manifold data through `SingularManifold`, singular homology
through `AlgebraicTopology.singularHomologyFunctor`, and integral bilinear forms through
`LinearMap.BilinForm`. A scoped source search found only a prose mention of intersection forms in
`Mathlib.Geometry.Manifold.Bordism`; it found no construction of an oriented four-manifold's
integral intersection pairing. The probe declares no theorem, axiom, proof, or proxy predicate and
receives no exact-statement credit.

The reused environment is Lean `4.29.0` (commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`) with mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The `lean-toolchain` and `lake-manifest.json`
SHA-256 values are respectively `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`
and `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
No update, build, clone, fetch, or dependency mutation was performed.

## Validation evidence

Commands ran from this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0584` | 0 | rank 625, planned, legacy artifacts unaccepted, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| pinned mathlib `rg` search for intersection-form and four-manifold APIs | 0 | only a prose mention in `Geometry/Manifold/Bordism.lean`; no intersection-pairing construction found |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0584/StatementInfrastructure.lean` | 0 | all five pinned infrastructure declarations elaborated and printed their types |
| `python3 -m json.tool Stage1_Instances/THM-M-0584/statement-blocker.json >/dev/null` | 0 | structured blocker is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0584` | 0 | no whitespace errors |

## Gate result

First failed gate: exact canonical-claim/source identity, before Lean target elaboration. Machine
status remains `M4`; no statement acceptance, proof credit, audit completion, or theorem completion
is claimed. Retry requires an immutable primary-source pin with exact theorem/page and independent
review, followed by a source-faithful implementation of the missing intersection-lattice surface.

Because the assigned statement phase is not complete, no `.stage1-worker-selftest.json` is emitted.
