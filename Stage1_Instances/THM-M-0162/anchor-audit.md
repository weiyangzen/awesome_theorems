# Anchor audit

Item: `S56-M-0162-ANCHOR_AUDIT`  
Base revision: `0a66013e1558a3bc4e31c9d7f64c0e8fb1dfebab`

## Audit boundary

The audited target is the elaborated expression
`Stage1Instances.THM_M_0162.FrenetSerretTarget`. This phase inventories formal anchors; it does not
accept a mathematical source, implement a proof, or change the target's `H1 / M4 / R4` debt.

## Pinned mathlib

`Formalizations/Lean/lake-manifest.json` pins mathlib to
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; the existing local package reports the same HEAD and a
clean status. A case-insensitive search of all pinned `Mathlib/**/*.lean` files for `Frenet`,
`Serret`, differential-geometric `torsion`, `curvature`, and `unit speed` found no exact or named
Frenet-Serret theorem. Algebraic torsion and connection-torsion hits are unrelated.

The useful anchors are supporting lemmas, not closure:

| Module | Checked declarations | Later role |
|---|---|---|
| `Mathlib.LinearAlgebra.CrossProduct` | `crossProduct`, `dot_self_cross`, `dot_cross_self`, `triple_product_permutation`, `cross_dot_cross`, `cross_cross_eq_smul_sub_smul` | oriented cross product and frame algebra |
| `Mathlib.Analysis.InnerProductSpace.Calculus` | `HasDerivAt.inner`, `deriv_inner_apply` | derivatives of orthogonality identities |
| `Mathlib.Geometry.Euclidean.Angle.Unoriented.CrossProduct` | `InnerProductGeometry.norm_toLp_symm_crossProduct` | Euclidean cross-product norm |

`AnchorAudit.lean` elaborates these names against the pinned environment. None has the canonical
target type, so none receives machine-proof credit.

## External Lean 4 search

Sourcegraph global Lean-language searches for `Frenet`, `Serret`, `FrenetSerret`, and
`frenet_serret` returned one relevant repository. The inspected immutable candidate is:

- repository: `https://github.com/facebookresearch/atlas-lean`
- revision: `34ffed396f376454c1a9b297f3fd74c5c801fb50`
- path: `Atlas/DifferentialGeometry/code/SpaceCurves.lean`
- downloaded source SHA-256: `58b6944dbd78a74f6cf978ead62b67a1e6202aedadac961f5a17a177aa7ef6d0`
- declarations: `SpaceCurves.frenetSerret_equation` (lines 645-670) and
  `SpaceCurves.frenetSerret_theorem` (lines 868-882 in the indexed source)

The candidate states a general-dimensional matrix equation for a Gram-Schmidt frame. It is not an
exact match: it carries a speed factor, uses generalized curvatures, does not identify the last
three-dimensional frame vector with the target's oriented cross product, and does not transport its
coefficients to `tau = -dot(B', N)`.

More decisively, the same source defines `SpaceCurves.frenetFrame_differentiableAt` with
`by sorry` at line 350. The later development invokes that declaration. Thus the attractive final
theorem is not acceptable terminal proof evidence even for its own statement, and it cannot be
imported or credited for this target. No dependency clone, fetch, or `.lake` mutation was performed.

The global search is reproducible discovery evidence, not a proof that no other Lean repository
exists. It is sufficient to classify every candidate actually found and to freeze the only relevant
external lead for later re-audit.

## Commands and results

Commands ran in this worker clone. The Lean command ran from `Formalizations/Lean` using only the
existing pinned `.lake` artifacts.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard valid; 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | ordered manifest valid |
| `python3 scripts/stage1_target.py show THM-M-0162` | 0 | rank 661, planned, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | exact manifest revision `8a178386...eea95` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | no output |
| `rg -n -i 'frenet|serret|torsion|curvature|unit.?speed' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 0 | no Frenet/Serret candidate; only unrelated or supporting hits |
| Sourcegraph API searches recorded above | 0 | only relevant result was `atlas-lean` at immutable commit `34ffed39...fb50` |
| immutable raw-file download plus `sha256sum` and `rg -n '\bsorry\b|\baxiom\b|\bunsafe\b'` | 0 | SHA-256 frozen; root-relevant `sorry` at line 350 |
| `lake env lean ../../Stage1_Instances/THM-M-0162/AnchorAudit.lean` | 0 | all pinned supporting declaration probes elaborated |
| `python3 -m json.tool ../../Stage1_Instances/THM-M-0162/anchor-audit.json` | 0 | structured audit is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0162` | 0 | no whitespace errors |

This anchor-audit phase is self-tested pending master acceptance. The root remains open: no exact
kernel-closed candidate was found, and no proof, `H0`, `M0`, `R0`, audit completion for the whole
theorem, or theorem completion is claimed.
