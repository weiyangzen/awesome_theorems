# Anchor-audit validation record

Item: `S56-M-0993-ANCHOR_AUDIT`  
Base revision: `8fae7de1ca4ed3b0645d51573ac87053fb300f40`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

Pinned mathlib at `8a178386ffc0f5fef0b77738bb5449d50efeea95` supplies an exact composite
route through `measure_ge_le_exp_mul_mgf`, `iIndepFun.integrable_exp_mul_sum`, and
`iIndepFun.mgf_sum`. `AnchorAudit.lean` independently restates the frozen root and elaborates that
composition for `Finset.univ`. Its axiom report contains only `propext`, `Classical.choice`, and
`Quot.sound`, with no `sorryAx`.

The legacy S1-M-273 wrapper is stronger but receives discovery credit only. The bounded external
search found special-purpose Hoeffding and small-ball uses of the same upstream declarations, not a
distinct exact terminal body. No external dependency is warranted because the exact route is already
inside the immutable local Lake closure. This is an `M0-L` candidate classification pending all
downstream gates; it is not theorem completion.

## Commands and results

All Lean commands used existing pinned artifacts. No Lake update/build, dependency fetch/clone, or
`.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0993` | 0 | rank 273, planned, legacy artifacts unaccepted, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | exact manifest pin `8a178386...ea95` |
| `rg` over repo-local and pinned Lean source | 0 | exact mathlib primitives and legacy direct wrapper located |
| Sourcegraph public search for the exact primitives and Chernoff phrase | 0 | 22 exhaustive query matches in five repositories; response SHA-256 `7381a397...1699` |
| immutable raw inspection of Atlas `Thm_1_9.lean` | 0 | different Hoeffding specialization; SHA-256 `fc6f3ec8...a028`; same Lean/mathlib pins |
| immutable raw inspection of `lean-stat-learning-theory` `SmallBallProb.lean` | 0 | different negative-tilt small-ball application; SHA-256 `01f48077...f032` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0993/AnchorAudit.lean` | 0 | exact three-declaration composition elaborated; no `sorryAx` in axiom report |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0993/Statement.lean` | 0 | frozen statement re-elaborated |
| `python3 Stage1_Instances/THM-M-0993/check_anchor_audit.py` | 0 | pin, module hash, clauses, route, candidates, and status boundary agreed |
| `python3 -m json.tool Stage1_Instances/THM-M-0993/anchor-audit.json` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0993 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Status boundary

The node is self-tested pending master acceptance. It supplies no H0, accepted obligation/proof node,
hermetic replay, independent receipt, or theorem-completion credit.
