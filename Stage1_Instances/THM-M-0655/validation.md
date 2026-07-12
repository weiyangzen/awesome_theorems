# Intake validation

Base revision: `3436a9512b8c720d6b89ba3b8a1d4c405ae3a95f`.

Validation is scoped to target membership, dossier structure and invariants, source-boundary
evidence, and whitespace. The repository wording does not yet determine an exact Lean proposition,
so no elaboration, kernel proof, source acceptance, or theorem completion is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0655` | exit 0; rank 700, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0655/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0655/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` (identity, rank, lifecycle, owned files, empty accepted states, and exact open dependency chain) |
| `git diff --check -- Stage1_Instances/THM-M-0655` | exit 0; no output |

Known downstream failures: exact source theorem/page and errata, resolution of possible duplication
with `THM-M-0654`, canonical Lean expression and environment fingerprint, language transports,
statement mutations, formal-anchor audit, obligation registry, proof, hermetic replay, and
independent review remain open. They prevent every theorem-completion claim but do not invalidate a
fail-closed `planned` intake.
