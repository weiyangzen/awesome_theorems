# Intake validation

Base revision: `d83bcd9bb91558d5f3e2cd99f964cc161d7a0cc5`.

Validation is limited to target-manifest consistency, dossier structure, scoped intake invariants,
the pinned Lean executable's availability, and whitespace. No canonical Lean proposition has been
selected, so no elaboration or kernel-proof result is claimed. No dependency update, fetch, or
`.lake` mutation was performed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1102` | exit 0; rank 542, planned, `L0/rework_required`, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `python3 -m json.tool Stage1_Instances/THM-M-1102/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1102/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1102` | exit 0; no output |

Known downstream failures: exact primary-source theorem identification, canonical statement, Lean
elaboration, expression and environment fingerprints, mutation tests, anchor audit, obligation
registry, proof, hermetic replay, and independent review remain open. They prevent theorem
completion but do not invalidate this truthful `planned` intake.
