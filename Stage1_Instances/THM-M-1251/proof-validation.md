# THM-M-1251 proof-phase validation

Item: `S56-M-1251-PROOF`  
Date: `2026-07-12` (Asia/Shanghai)  
Base revision: `33a031b5238cc674b8e1073106bff2685c6bbbc4`

## Implemented proof

`Proof.lean` closes the exact frozen pointwise-dual proposition. For every
finite-dimensional real normed space `E`, the theorem
`importedDefinitionExpansion` introduces the four binders and proves

```text
TemperedDistribution E Complex = (SchwartzMap E Complex →Lₚₜ[Complex] Complex)
```

by `rfl`. This is the pinned mathlib definition at
`Mathlib.Analysis.Distribution.TemperedDistribution#TemperedDistribution`, not
an assumed equality. `temperedDistributionsAreSchwartzDual` is the explicit
child-to-root composition certificate. The wrapper does not broaden the
domain or substitute a strong-dual representation theorem.

The machine proof cut for `M1251-ROOT` is closed. This proof receipt does not
claim full theorem completion: the frozen registry's human source, readable
reconstruction, foundation/provenance, validation, independent verification,
release, and master-acceptance gates remain downstream.

## Exact validation

The following commands ran in the worker clone. The existing canonical pinned
`.lake` artifacts were reused; no update, build, dependency clone, or fetch was
run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets pass. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets, ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-1251` | 0 | Rank 171, planned, theorem incomplete. |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1251/Statement.lean` | 0 | Frozen target re-elaborates and prints its explicit expression. |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1251/ObligationTree.lean` | 0 | Frozen conditional composition re-elaborates. |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1251/Proof.lean` | 0 | Both exact proof declarations elaborate; both axiom probes report only `propext`, `Classical.choice`, and `Quot.sound`, with no `sorryAx`. |
| `python3 Stage1_Instances/THM-M-1251/check_proof.py` | 0 | Receipt, source hash, exact declarations, proof body, and prohibited-token checks pass. |
| `git diff --check -- Stage1_Instances/THM-M-1251 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; `lean-toolchain` SHA-256
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`;
`lake-manifest.json` SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

Status boundary: genuine self-tested proof-phase closure, pending integration
lane acceptance. It supplies no validation-phase or theorem-release claim.
