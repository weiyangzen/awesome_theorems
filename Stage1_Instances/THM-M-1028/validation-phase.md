# S56-M-1028-VALIDATION worker evidence

Date: `2026-07-12`

Base revision: `8509654fd1347228b71158b61f9f700360aa1691`

The validation phase re-elaborated the exact statement and the proof phase's
conditional composition. `Validation.lean` independently reconstructs the
modification algebra, full-measure event intersection, and conditional root
composition without importing `Proof.lean`. The validator also checks the
frozen statement hash, 16-node obligation denominator, typed-graph open-root
boundary, toolchain and Lake pins, local placeholder/unsafe policy, and kernel
axiom output.

This is partial validation, not full-root or release validation. The first
failed node gate is the proof dependency: `M1028-C-CONTINUOUS-MODIFICATION` and
`M1028-T-NONDIFFERENTIABLE` are still `M4`. Thus the root remains `M2`, and
`audit_complete=false` and `theorem_complete=false`. The same-checkout probe is
useful independence evidence but does not meet the distinct-runner gate.

## Commands and exact results

All commands ran from the worker clone. The pre-existing canonical `.lake`
symlink was reused; no update, build, fetch, clone, or network operation ran.

```text
$ python3 Docs/tools/check_stage1_standard.py
check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)
exit 0

$ python3 scripts/stage1_target.py check
stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)
exit 0

$ python3 scripts/stage1_target.py show THM-M-1028
exit 0; rank 221, planned, L0/rework_required, theorem_complete false

$ python3 Stage1_Instances/THM-M-1028/check_statement.py
exit 0; four scope mutations killed; pinned Lean 4.29.0/mathlib identity reported

$ python3 Stage1_Instances/THM-M-1028/check_obligation_tree.py
PASS THM-M-1028 obligation tree: 16 obligations, 35 typed edges
root closure: open (M2); continuity and nowhere-differentiability packages remain M4
exit 0

$ python3 Stage1_Instances/THM-M-1028/check_proof.py
PASS THM-M-1028 proof source: 5 checked bodies; exact root remains conditional on 2 open packages
exit 0

$ python3 Stage1_Instances/THM-M-1028/check_validation.py
validation ok: exact conditional composition kernel-replayed; independent probe passed; root remains open (M2)
exit 0

$ (cd Formalizations/Lean && lake env lean --version)
Lean (version 4.29.0, x86_64-unknown-linux-gnu, commit 98dc76e3c0a9b856c9b98726b713fb04fab16740, Release)
exit 0

$ git diff --check -- Stage1_Instances/THM-M-1028 .stage1-worker-selftest.json
exit 0; no output
```

The kernel reports only `propext`, `Classical.choice`, and `Quot.sound` for
the checked conditional composition declarations, and no `sorryAx`.
