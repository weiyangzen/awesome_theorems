# THM-M-0540 proof-phase validation

Item: `S56-M-0540-PROOF`  
Date: `2026-07-12` (Asia/Shanghai)  
Base revision: `be98a856ad5cbf322fb2fda71f1506bd05f1d355`

## Implemented closure

`Proof.lean` repeats the exact frozen proposition because the dossier is outside the Lake source
tree. `unfoldingEquation` closes `M0540-T-UNFOLD` by reducing the two local abbreviations and the
pinned definition of `AlgebraicTopology.singularHomologyFunctor`. The root declaration explicitly
consumes that terminal result, supplying the child-to-root composition certificate.

This closes all six frozen machine obligations without changing the small-space domain, natural
grading, integer coefficients, or equality conclusion. It does not close the separately frozen
human-source, readable, provenance, trust, validation, or release gates.

## Exact validation

All commands ran in the worker clone. Existing canonical pinned `.lake` artifacts were reused; no
update, build, dependency clone, or fetch was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets, ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-0540` | 0 | Rank 597; planned; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0540/check_obligation_tree.py` | 0 | Frozen nine-obligation registry and 24 typed edges passed. |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0540/Statement.lean` | 0 | Frozen exact target re-elaborated. |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0540/ObligationTree.lean` | 0 | Frozen conditional composition re-elaborated. |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0540/Proof.lean` | 0 | Terminal equation and exact root elaborated; both reports list only `propext`, `Classical.choice`, and `Quot.sound`. |
| `python3 Stage1_Instances/THM-M-0540/check_proof.py` | 0 | Receipt hashes, obligations, declarations, and prohibited-token checks passed. |
| `git diff --check -- Stage1_Instances/THM-M-0540 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

Pinned environment: Lean `4.29.0`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; `lean-toolchain` SHA-256
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`;
`lake-manifest.json` SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

Status boundary: genuine self-tested proof-phase root closure pending integration-lane acceptance.
No validation-phase or theorem-completion claim is made.
