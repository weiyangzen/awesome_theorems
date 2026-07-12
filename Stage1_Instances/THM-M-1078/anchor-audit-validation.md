# Anchor-audit validation record

Item: `S56-M-1078-ANCHOR_AUDIT`

Base revision: `40b00afc847f5216750db3225d428712dd401350`

## Result

The audit found no exact theorem in the pinned mathlib revision. It found one credible external
Lean 4 formalization, `SmaniaD/Burkholder` at immutable commit
`afa97ef3c85697fa3b2a67af89af8d6dd09eda69`. Its
`MeasureTheory.Lp_Burkholder_inequality_martingaleTransform` is a substantive near match, not an
exact wrapper for the frozen statement. The six concrete statement and integration differences are
recorded in `anchor-audit.json`; consequently the root remains `M2`, not `M0-P`.

The external archive was downloaded only to `/tmp` for inspection. It was not cloned, built, or
added to `.lake`. The upstream passing badge is discovery evidence, not local kernel evidence.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95`, equal to the Lake manifest pin |
| `rg -n -i 'martingale.?transform\|burkholder\|transform.*martingale\|martingale.*transform' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | no named exact theorem; bounded negative source-tree search |
| `rg -n 'Submartingale.sum_(smul\|mul)_sub' Formalizations/Lean/.lake/packages/mathlib/Mathlib/Probability/Martingale/Basic.lean` | 0 | supporting transform-closure declarations at lines 540, 574, 580, and 589 |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1078/AnchorAudit.lean` | 0 | all selected pinned mathlib declarations elaborated and their types printed |
| `curl ... GitHub repository searches` plus `sha256sum` | 0 | both queries found only `SmaniaD/Burkholder`; response SHA-256 `14b6d0...78a5` |
| `curl ... Sourcegraph search stream` plus `sha256sum` | 0 | `matchCount=0`; response SHA-256 `4f7c6803...9e56`; bounded result only |
| `git ls-remote https://github.com/SmaniaD/Burkholder.git refs/heads/main refs/tags/'*'` | 0 | main `afa97ef...da69`; tag `v0.1.0`, peeled `fd97e5...b389` |
| `curl ... codeload .../afa97ef...da69` plus `sha256sum` | 0 | immutable archive SHA-256 `d3b0dbda...0a60` |
| `rg -n '\bsorry\b\|\badmit\b\|axiom\|unsafe\|debug.skipKernelTC' /tmp/thm1078-burkholder --glob '*.lean'` | 1 | no matched placeholder, explicit axiom, unsafe declaration, or kernel-skip marker |
| `python3 -m json.tool Stage1_Instances/THM-M-1078/anchor-audit.json` | 0 | JSON valid |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets valid |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1078` | 0 | rank 520, planned, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-1078 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Status boundary

This is self-tested anchor-audit evidence pending master acceptance. It does not prove the target.
The obligation-tree, proof, exact external integration, trust, hermetic, and release gates remain
open. GitHub code search was rate-limited; this is recorded as a bounded search failure rather than
a false negative result.
