# Intake validation

Base revision: `68bccb854a8ce9bdd5fbdfdda203abe0bb3819eb`.

Validation is limited to target-set consistency, dossier syntax and scoped intake invariants. The
authoritative metadata does not identify one proposition, so a Lean declaration would necessarily
encode an invented variant or abstract proxy. No elaboration, source review, kernel proof, audit
completion, or theorem completion is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0185` | exit 0; rank 672, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0185/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0185/task-dag.json` | exit 0 |
| scoped Python assertions over the manifest, instance, DAG, required files, and crosswalk boundary | exit 0; `intake invariant check: ok` |
| scoped Python trailing-whitespace and final-newline assertions over all owned files | exit 0; `owned text check: ok` |

Known downstream failures are the unresolved pinpoint source theorem, exact canonical claim,
profiles, Lean expression and environment fingerprint; source review, statement mutations, formal
candidate audit, obligation registry, proof, hermetic replay, and independent verification also
remain open. These prevent every later phase and theorem completion, but do not invalidate this
truthful `planned` intake.
