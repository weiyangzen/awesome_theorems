# THM-M-1005 proof execution

Item: `S56-M-1005-PROOF`  
Date: `2026-07-12` (`Asia/Shanghai`)  
Base revision: `31c0253e7592e9a19dd9571adcf10eb0023effda`

## Verdict

`blocked`. `Proof.lean` adds three genuine placeholder-free proof bodies. `absSubmartingale`
normalizes a real martingale to the nonnegative submartingale `|f|` using the supremum of `f` and
`-f`. `measurable_runningAbsMax` proves measurability of the inclusive finite maximum.
`weakMaximal_abs` then applies pinned `MeasureTheory.maximal_ineq` to that absolute process with the
exact running maximum from the frozen statement.

These bodies close `M1005-N-ABS-SUBMARTINGALE`, `M1005-C-MAXIMUM`, and
`M1005-L-WEAK-MAXIMAL`, but not the assigned proof phase. The first unavailable analytic leaf is
`M1005-L-LAYER-CAKE`; `M1005-L-HOLDER` and `M1005-L-CONSTANT` also remain open. Consequently no
body inhabits `M1005-T-STRONG-ESTIMATE`, the canonical root remains open at `M3`, and no exact
strong `L^p` theorem or theorem completion is claimed. `.stage1-worker-selftest.json` is
deliberately absent because the assigned proof deliverable is incomplete.

## Narrow validation evidence

All commands ran in this worker clone and reused the existing pinned Lake artifacts. No update,
build, dependency clone/fetch, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1005` | 0 | rank 285, planned, L0/rework-required, theorem incomplete |
| `python3 Stage1_Instances/THM-M-1005/check_obligation_tree.py` | 0 | 14 obligations and 48 typed edges passed; frozen pre-proof root open `M3` |
| `python3 Stage1_Instances/THM-M-1005/check_statement.py` | 0 | exact expression hash `32343e66034f94d4afabc10f4d15cbae77daf650c757023a2142aafba50366e5`; four mutations distinguished |
| temporary `Statement.olean`, then `LEAN_PATH=<temporary>:$(lake env printenv LEAN_PATH) lake env lean ../../Stage1_Instances/THM-M-1005/Proof.lean` from `Formalizations/Lean` | 0 | all three declarations elaborated; each axiom report was exactly `propext`, `Classical.choice`, `Quot.sound` |
| forbidden-token scan of `Proof.lean` | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, or `unsafe` |
| `sha256sum Stage1_Instances/THM-M-1005/{Statement.lean,Proof.lean}` | 0 | statement `03e36de9...f38f6`; proof `d041cfaf...036d` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git diff --check -- Stage1_Instances/THM-M-1005` | 0 | no whitespace errors |

## Reopen condition

Resume after implementing the remaining frozen layer-cake, Holder, and constant obligations, or
after locating an immutable exact Lean 4 strong-Doob proof whose type, terminal body, trust closure,
and local pinned integration all validate. A related weak theorem cannot close this target.
