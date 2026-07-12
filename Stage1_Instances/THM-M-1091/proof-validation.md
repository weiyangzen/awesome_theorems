# THM-M-1091 proof-phase validation

Item: `S56-M-1091-PROOF`  
Date: `2026-07-12` (`Asia/Shanghai`)  
Base revision: `032d685539fcd91ec6eeb889a18ff62f3f936a41`

## Verdict

`self_tested_pending_master_acceptance`. `Proof.lean` supplies a placeholder-free proof body for
the exact `ChapmanKolmogorovTarget` frozen in `Statement.lean`. It instantiates pinned mathlib
`Kernel.pow_add` at `n,m`, then uses only addition commutativity to reconcile mathlib's displayed
composition order with the frozen chronological order. The checked statement transport also
produces the exact setwise integral equation.

This closes the frozen proof-phase machine cut, including `M1091-L-POWADD` and the exact root, but
does not claim theorem completion. Human-source fidelity remains `H1`; downstream validation,
release, trust, readability, freshness, independent verification, and master acceptance remain
open.

## Narrow validation evidence

All commands ran in this worker clone using the existing pinned Lake artifacts. No `lake update`,
build, dependency clone/fetch, or other `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1091` | 0 | rank 533; planned; hard mathlib anchor/wrapper lane; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1091/check_obligation_tree.py` | 0 | 12 obligations and 16 typed edges passed; frozen pre-proof cut is `M1091-L-POWADD` |
| `python3 Stage1_Instances/THM-M-1091/check_proof.py` | 0 | exact root, pinned anchor invocation, index normalization, integral transport, and status boundary found; forbidden tokens absent |
| `python3 -m json.tool Stage1_Instances/THM-M-1091/proof.json` | 0 | structured proof receipt parses |
| `cd Stage1_Instances/THM-M-1091 && LEAN_PATH=".:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)" ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lake env lean -o Statement.olean Statement.lean` | 0 | exact frozen statement and checked transports elaborated into a temporary target-local module |
| `cd Stage1_Instances/THM-M-1091 && LEAN_PATH=".:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)" ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lake env lean Proof.lean` | 0 | exact root and integral theorem elaborated; each axiom report was `[propext, Classical.choice, Quot.sound]` |
| `rm -f Stage1_Instances/THM-M-1091/Statement.olean` | 0 | temporary target-local elaboration artifact removed |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git diff --check -- Stage1_Instances/THM-M-1091 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Status boundary

The assigned proof phase has a real kernel-elaborated body for the exact frozen root and is ready
for integration review. This worker does not alter authoritative workflow state or accept a
receipt. `THM-M-1091` remains theorem-incomplete until every later rev-5.6 gate is accepted.
