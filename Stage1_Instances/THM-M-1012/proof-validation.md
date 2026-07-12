# THM-M-1012 proof-phase validation

Item: `S56-M-1012-PROOF`  
Date: `2026-07-12` (`Asia/Shanghai`)  
Base revision: `e4f68760f8779f934ed18b07dad15e4512436d06`

## Implemented proof bodies

`Proof.lean` imports the exact frozen statement and obligation interfaces. `pinnedForward` and
`pinnedReverse` project the two implications from the exact pinned declaration
`MeasureTheory.ProbabilityMeasure.tendsto_iff_tendsto_charFun`. The proof then uses the previously
frozen `ObligationTree.root_of_directions` composition body and inhabits
`LevyContinuityKnownLimitTarget` without changing any binder, hypothesis, topology, coercion, or
conclusion.

The four declarations elaborate without placeholders and report exactly `propext`,
`Classical.choice`, and `Quot.sound`. This self-tests the assigned proof node only. The immutable
obligation-tree artifact still truthfully records its pre-proof `M3` observation; this phase does
not rewrite prior evidence or claim master acceptance, validation, H0/R0, hermetic replay,
independent verification, release, or theorem completion.

## Commands and exact results

All commands ran in this worker clone using the existing pinned Lake artifacts. No `lake update`,
`lake build`, dependency clone/fetch, network operation, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `bash Stage1_Instances/THM-M-1012/check_proof.sh` | 0 | isolated temporary oleans for `Statement.lean` and `ObligationTree.lean`; `Proof.lean` elaborated; all four declarations reported only the three allowed axioms above |
| `python3 Stage1_Instances/THM-M-1012/check_proof.py` | 0 | exact pinned directions, frozen root composition, exact statement root, forbidden-token scan, and four axiom probes passed; proof SHA-256 `db7727c0babbd6d0d03e484d5f71fe955c7864caf6403dd69bde6d59c1d1cec7` |
| `python3 Stage1_Instances/THM-M-1012/check_obligation_tree.py` | 0 | 14 frozen obligations and 61 typed edges passed; denominator `b62eb6e1869e2c7db9f45ad1ea1e5b467280a9a2fd75a339916b7c5a5815edfb` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1012` | 0 | rank 291, planned, legacy artifacts unaccepted, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git diff --check -- Stage1_Instances/THM-M-1012 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Status boundary

The proof deliverable is self-tested and ready for integration-lane inspection. Only the master may
accept its provisional state. The validation and release phases, primary-source closure, readable
reconstruction, hermetic replay, and independent review remain downstream, so theorem completion
remains false.
