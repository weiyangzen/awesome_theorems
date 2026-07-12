# Intake validation

Base revision: `56f664bd25214d40605c0b36e238c3e0cd9f1d9d`.

Validation is limited to repository/manifest consistency, dossier structure, JSON syntax, scoped
planned-intake invariants, and whitespace. No exact Lean expression has been selected; therefore a
`lake env lean` elaboration would test an invented or broadened statement and is deliberately not
claimed as kernel evidence.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0572` | exit 0; rank 618, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0572/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0572/task-dag.json` | exit 0 |
| scoped Python intake assertions over identity, lifecycle, root vector, accepted states, owned file set, six open downstream tasks, and first dependency | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0572` | exit 0; no output |

Known downstream failures: the exact primary-source theorem/page, assumptions, and errata have not
been inspected; real/complex and geometric conventions are open; no canonical Lean expression,
anchor audit, obligation registry, proof, hermetic replay, or independent review exists. These
prevent theorem completion but do not invalidate this fail-closed planned intake.
