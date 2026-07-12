# Intake validation

Base revision: `e3d0fd205c9c81486cb86f68cdc66d4d4e5bb264`.

All commands ran from the worker clone on 2026-07-12. The shared canonical `.lake` symlink was used
read-only; no dependency update, fetch, clone, or build was run. Validation covers target
membership, dossier structure, JSON integrity, whitespace, and a narrow pinned Lean API probe. It
does not establish an exact Chebotarev statement or proof.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0019` | 0 | rank 897, planned, L0/rework_required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0019/instance.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0019/task-dag.json` | 0 | valid JSON |
| scoped Python intake assertions | 0 | IDs, planned lifecycle, null target, empty accepted state, open downstream DAG, and false completion flags agree |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0019/IntakeProbe.lean)` | 0 | six nearby pinned number-field, ideal, and conjugacy APIs elaborated under Lean 4.29.0 |
| `rg -ni 'chebotarev|chebotaryov|tschebotareff' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 1 | bounded pinned mathlib name search returned no matches; not a comprehensive anchor audit |
| `git diff --check -- Stage1_Instances/THM-M-0019` | 0 | no whitespace errors |

Known downstream failures remain deliberately open: pinpoint primary-source inspection and review,
exact statement and density encoding, elaborated expression and mutation tests, discovery and
obligation freezes, formal candidate audit, proof, hermetic replay, and independent release
verification. They prevent theorem completion but do not invalidate a truthful `planned` intake.
