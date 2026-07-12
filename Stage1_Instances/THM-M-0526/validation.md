# Intake validation

Base revision: `5b43761c4dbd9f2e8ac27059f1a5ed797a694d8e`.

Validation is limited to manifest consistency, dossier structure, scoped intake invariants, JSON,
and whitespace. No canonical Lean expression has been selected, so running `lake env lean` would
not validate a theorem statement and no kernel result is claimed. The existing `.lake` directory
is an untracked worker-clone artifact and was inspected but not modified.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0526` | exit 0; rank 583, no legacy slot, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0526/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0526/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok`; exact file set, target identity, lifecycle, rank, L0 baseline, empty accepted states, open linear downstream DAG, and forbidden-token scan passed |
| `git diff --check -- Stage1_Instances/THM-M-0526` | exit 0; no output |

Known downstream failures: exact primary-source inspection and independent review, canonical Lean
elaboration and mutation tests, formal-candidate audit, obligation registry, proof, hermetic replay,
and independent release validation remain open. They prevent theorem completion but do not
invalidate a truthful planned intake.
