# Statement validation record

Item: `S56-M-1188-STATEMENT`  
Base revision: `31b7ab5b3902c4a80878c2007218f90566a8b85c`

## Frozen target

`Stage1Instances.THM_M_1188.HeatEquationWeakMaximumPrincipleTarget` freezes the classical weak
maximum principle on a nonempty bounded open subset of `EuclideanSpace Real (Fin n)`, with `n >= 1`
and `T > 0`. The closed cylinder is `closure U x [0,T]`; the parabolic boundary is the initial face
plus `frontier U x [0,T]`, deliberately excluding the terminal face over the interior. Spatial and
temporal classical regularity and `u_t - Laplacian u <= 0` are explicit.

The conclusion uses an attained boundary witness that dominates every point of the closed cylinder.
`target_iff_pointwiseMaximumForm` kernel-checks its direct pointwise expansion. The only direct
import is `Mathlib.Analysis.InnerProductSpace.Laplacian`.

## Commands and results

Lean commands ran from `Formalizations/Lean` using the existing pinned `.lake` environment; no
dependency update, fetch, build, or mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1188/Statement.lean` | 0 | canonical target, checked transport, four structural mutations, and initial-face boundary theorem elaborated; explicit target printed |
| `python3 ../../Stage1_Instances/THM-M-1188/check_statement.py` | 0 | expression SHA-256 `0564abe47c982ec2eea57b707d8e761b8f00999b3d35fc307f18e406c163ffd8`; all four mutations distinguished; mathlib revision matched |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum Stage1_Instances/THM-M-1188/Statement.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `1e84c9...a4b0`, `651c8a...1d2`, and `321626...5b2` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard valid: 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1188` | 0 | rank 383; planned; hard-mathlib-anchor-and-wrapper lane |
| `python3 -m json.tool Stage1_Instances/THM-M-1188/statement.json` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1188` | 0 | no whitespace errors |

## Mutation and status boundary

The validator serializes explicit elaborated expressions and distinguishes removal of the PDE
hypothesis, restriction to dimension one, rebinding the boundary witness separately for each
cylinder point, and inclusion of the forbidden terminal face. The boundary theorem checks that
`closure U x {0}` is genuinely included in the selected parabolic boundary.

This is self-tested statement evidence pending master acceptance. It does not inspect a proof body
or claim source fidelity, theorem closure, audit completion, or release readiness.
