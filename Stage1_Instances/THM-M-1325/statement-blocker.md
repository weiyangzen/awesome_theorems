# Statement gate blocker

Item: `S56-M-1325-STATEMENT`  
Theorem: `THM-M-1325`  
Verdict: blocked; no exact canonical Lean target is claimed.

## First failed gate

The authoritative source record gives only the name "Bishop-Gromov volume comparison" and the
phrase "Ricci curvature and volume." The intake supplies the standard ratio-monotonicity family,
but explicitly leaves primary-source inspection and the exact theorem/page crosswalk open. It does
not determine the normalization and sign of Ricci curvature, dimension and regularity assumptions,
completeness versus a local ball hypothesis, open or closed balls, the model-volume normalization,
or the source-valid radius domain (especially for positive model curvature).

Those choices change the proposition. Selecting them from a modern recollection would invent
missing source mathematics, while replacing ratio monotonicity with the absolute Bishop upper bound
would substitute a weaker theorem. Thus ordered binders, hypotheses, conclusion, checked transports,
expression fingerprint, and meaningful statement mutations cannot truthfully be frozen.

There is also a concrete pinned-library blocker. A case-insensitive search of the checked mathlib
tree finds no declaration or documentation occurrence for Ricci curvature, sectional curvature, or
a curvature tensor. Its Riemannian-manifold directory contains only `PathELength.lean` and
`Basic.lean`; `Basic.lean` provides Riemannian distance but not Ricci curvature or a manifold
Riemannian volume measure. Generic `Measure`, `Measure.restrict`, and `Metric.ball` do not supply
those missing geometric definitions. Defining them ad hoc in this phase would not be a minimal-import
elaboration of the exact target.

`StatementInfrastructure.lean` checks only the available Riemannian-manifold, metric-ball, and
generic-measure interfaces. It deliberately declares no canonical proposition, theorem, axiom,
placeholder, proxy curvature predicate, or assumed conclusion.

## Environment fingerprint

- Repository base revision: `1cad5fb04b4f845438a8105579b15a830b03b7e7`.
- Validation date: 2026-07-12.
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean `4.29.0`, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- mathlib checked revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- Lake manifest SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Validation evidence

Lean commands ran against the existing pinned `.lake` artifacts. No update, fetch, clone, or build
command was used.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1325/StatementInfrastructure.lean` | 0 | the available `IsRiemannianManifold`, `Metric.ball`, `Measure`, and `Measure.restrict` interfaces elaborated |
| `rg -n -i '\\bRicci\\b|sectional curvature|curvature tensor' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 1 | no matches in pinned mathlib |
| `find Formalizations/Lean/.lake/packages/mathlib/Mathlib/Geometry/Manifold/Riemannian -maxdepth 2 -type f -print` | 0 | only `PathELength.lean` and `Basic.lean` |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes match the environment fingerprint above |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1325` | 0 | rank 487, planned, L0/rework-required, theorem incomplete |

## Retry condition

Preserve and audit an immutable source edition with a pinpoint theorem and freeze every convention
listed above. Then either pin a Lean 4 dependency that implements the required Ricci tensor,
Riemannian volume, constant-curvature model, and comparison statement, or first implement and
kernel-validate those APIs under their own obligations. Only then can the exact proposition be
elaborated with minimal imports and subjected to transport and mutation checks.

Until those inputs exist, the statement gate remains at `M4`; statement acceptance and theorem
completion are false. The existing intake and execution DAG are not modified. Because the assigned
phase is not genuinely self-tested to completion, no `.stage1-worker-selftest.json` is emitted.
