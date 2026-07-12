# Intake validation

Base revision: `d41c33c7ad196cf30c996231fabd214f4d9f5248`.

The preflight worktree contained the untracked shared link/path `Formalizations/Lean/.lake`; it was
not created or modified by this intake. Consequently these checks are scoped, nonrelease evidence.
Validation covers target membership, dossier structure, the planned-state invariants, and text
integrity. No canonical Lean expression has been selected, so no kernel proof result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0319` | exit 0; rank 685, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0319/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0319/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0319` | exit 0; no output |

Known downstream failures are intentional and explicit: exact primary-source theorem/page and
errata review, canonical Lean elaboration, environment fingerprint, checked alternate transports,
anchor audit, obligation registry, proof, hermetic replay, and independent review remain open. They
prevent audit and theorem completion but do not invalidate this fail-closed planned intake.
