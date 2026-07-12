# THM-M-0318 anchor-audit validation

Item: `S56-M-0318-ANCHOR_AUDIT`  
Base revision: `ba66c12eb0b1828b8aa19b6fa8eb2171a454e162`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

The pinned mathlib revision contains no Schauder fixed-point declaration. The strongest nearby
checked anchors are the Banach contraction theorem on a complete invariant subset and the
one-dimensional interval fixed-point theorem. The first assumes contraction, and the second is
only an interval special case. Neither is a valid substitute for the frozen arbitrary-dimensional
compact-convex target.

The external search located `harfe/fixed-point-theorems-lean4` at immutable revision
`11a9f041...d5e4`. Its `brouwer_fixed_point` source proves the finite-dimensional compact-convex
case, but explicitly assumes `FiniteDimensional Real V`. It uses Lean `4.21.0-rc3`, mathlib
`c873c5d...0b7cb`, is outside the local closure, and was source-audited rather than fetched or
built. It therefore supplies an `E3` branch anchor, not root closure.

The canonical root remains `M3`: its exact statement is elaborated, but no root proof artifact was
located. This completes this candidate-audit phase pending master acceptance and makes no theorem,
full-audit, or release claim.

## Commands and exact outcomes

| Command | Exit | Outcome |
|---|---:|---|
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty; pinned package worktree clean |
| `rg -n -i 'schauder|fixed.?point|FixedPoint|fixedPoint' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 0 | Schauder hits were basis API only; fixed-point results were narrower, including contraction and interval results |
| `git ls-remote https://github.com/harfe/fixed-point-theorems-lean4.git refs/heads/main` | 0 | resolved `11a9f041246d28374edae384241757f9a0cbd5e4` |
| immutable raw inspection of `FixedPointTheorems/brouwer.lean`, `lean-toolchain`, and `lake-manifest.json` | 0 | finite-dimensional theorem, Lean `4.21.0-rc3`, mathlib `c873c5d...0b7cb` matched |
| `lake env lean ../../Stage1_Instances/THM-M-0318/AnchorAudit.lean` from `Formalizations/Lean` | 0 | both nearby declarations elaborated; both report `propext`, `Classical.choice`, and `Quot.sound` |
| `python3 ../../Stage1_Instances/THM-M-0318/check_anchor_audit.py` from `Formalizations/Lean` | 0 | local pin/source inventory and immutable external candidate matched; root remained `M3` |
| `python3 -m json.tool Stage1_Instances/THM-M-0318/anchor-audit.json` | 0 | structured ledger valid |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets valid |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0318` | 0 | rank 684, planned, theorem completion false |
| `git diff --check -- Stage1_Instances/THM-M-0318 .stage1-worker-selftest.json` | 0 | no whitespace errors |

No `lake update`, dependency clone/fetch/build, or `.lake` mutation was performed. GitHub's
unauthenticated code-search endpoint and grep.app rate-limited broad code queries; this limitation
is preserved in the structured search record rather than silently treated as exhaustive proof of
nonexistence.
