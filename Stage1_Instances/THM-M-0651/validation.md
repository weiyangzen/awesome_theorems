# Intake validation

Base revision: `3436a9512b8c720d6b89ba3b8a1d4c405ae3a95f`.

Validation is limited to target/standard consistency, dossier structure, scoped intake invariants,
the available pinned environment, and whitespace. The pre-existing untracked
`Formalizations/Lean/.lake` link/artifact makes this a dirty nonrelease run. No canonical Lean
expression exists yet, so no kernel theorem result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0651` | exit 0; rank 697, L0/rework_required, planned, theorem_complete false |
| `cd Formalizations/Lean && lake env lean --version` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; pinned mathlib tree `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `python3 -m json.tool Stage1_Instances/THM-M-0651/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0651/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0651` | exit 0; no output |

Known downstream failures: pinpoint primary-source inspection and independent review; exact
partial-type, nonprincipality, countability, and omission definitions; canonical Lean elaboration
and mutation tests; anchor audit; obligation registry; proof; hermetic replay; and release receipts
remain open. These prevent audit and theorem completion but do not invalidate a fail-closed planned
intake.
