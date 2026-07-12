# Intake validation

Base revision: `d7b1a45d1590cdafe55436182144e1f35e6b4194`.

Validation is limited to repository/manifest consistency, dossier structure, scoped intake
invariants, and whitespace. No canonical Lean expression has been selected in this intake phase,
so no elaboration or kernel result is claimed. The existing `Formalizations/Lean/.lake` entry was
already untracked at preflight and was not modified or used as proof evidence.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0168` | exit 0; rank 665, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0168/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0168/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok`; checked identity, lifecycle, baseline, rank, empty acceptance, debt vector, artifact inventory, and ordered open DAG |
| direct trailing-whitespace assertion over owned files | exit 0; included in the scoped Python check because this new dossier is untracked and therefore absent from ordinary `git diff --check` output |
| `git diff --check -- Stage1_Instances/THM-M-0168` | exit 0; no output |

Known downstream failures: pinpoint primary-source inspection and errata review, exact regularity
and minimality selection, an exact Lean target and checked geometric/PDE transports, mutation tests,
formal-candidate audit, obligation expansion, proof, hermetic replay, and independent review remain
open. They prevent theorem completion but do not invalidate this fail-closed planned intake.
