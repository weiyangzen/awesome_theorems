# Intake validation

Base revision: `c8bb1d8f046a4b2816eb059edc201b88d2063f42`.

Validation is limited to repository/manifest consistency, dossier structure, scoped intake
invariants, and whitespace. No canonical Lean expression has been selected in this intake phase,
so no elaboration or kernel result is claimed. The existing `Formalizations/Lean/.lake` entry was
already untracked at preflight and was not modified or used as proof evidence.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0158` | exit 0; rank 657, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0158/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0158/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok`; checked identity, lifecycle, baseline, rank, empty acceptance, debt vector, artifact inventory, and the ordered open DAG |
| `git diff --check -- Stage1_Instances/THM-M-0158` | exit 0; no output (the dossier was untracked, so the final self-test also applies a direct whitespace assertion to its files) |

Known downstream failures: pinpoint primary-source inspection, source convention and errata review,
exact Lean statement and mutation tests, formal-candidate audit, obligation expansion, proof,
hermetic replay, and independent review remain open. They prevent theorem completion but do not
invalidate this fail-closed planned intake.
