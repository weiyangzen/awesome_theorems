# Intake validation

Base revision: `fe921f79cbbe97438c1012a2a3d06e4f2bf2daf0`.

Validation is limited to repository/manifest consistency, dossier structure, scoped intake
invariants, repository-local discovery, and whitespace. There is no canonical Lean expression in
this phase, so `lake env lean` would have no truthful target to elaborate and no kernel result is
claimed. The existing untracked `Formalizations/Lean/.lake` link/artifact predates this work and was
not modified.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0606` | exit 0; rank 644, planned, L0/rework_required, theorem_complete false |
| `rg -n 'Kervaire\|HomotopySphere\|homotopy sphere\|ExoticSphere' Formalizations/Lean --glob '!**/.lake/**'` | exit 0; adjacent homotopy-sphere material only; no target-specific Kervaire-Milnor declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0606/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0606/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0606` | exit 0; no output |

Known downstream failures are intentional and fail closed: exact primary-source theorem/page and
errata review, canonical Lean elaboration, mutation tests, anchor audit, obligation registry, proof,
hermetic replay, and independent review remain open. They prevent audit and theorem completion but
do not invalidate this self-tested `planned` intake.
