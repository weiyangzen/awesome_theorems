# Intake validation

Base revision: `64b3d9781c233011aa06d7899ba7c31e8ef481ee`.

Validation is limited to target-set consistency, dossier structure, scoped intake invariants, the
available pinned Lean executable, and whitespace. No canonical Lean expression has been selected,
so no elaboration or kernel-proof result is claimed. Existing `.lake` artifacts were used read-only;
no update, build, clone, or fetch command was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0320` | exit 0; rank 686, planned, L0/rework_required, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| pinned-mathlib `rg` search for `Kakutani`, set-valued fixed points, and upper hemicontinuity | exit 0 overall; upper-hemicontinuity API located, no Kakutani fixed-point declaration located |
| `python3 -m json.tool Stage1_Instances/THM-M-0320/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0320/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0320 .stage1-worker-selftest.json` | exit 0; no output |

Known downstream failures are immutable primary-source inspection and independent review, exact
Lean statement and mutation tests, formal-anchor audit, obligation registry, proof, hermetic replay,
and release validation. They prevent theorem completion but do not invalidate this truthful planned
intake.
