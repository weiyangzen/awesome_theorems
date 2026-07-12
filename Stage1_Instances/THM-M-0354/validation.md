# Intake validation

Base revision: `cc46a50150dae27c90dca0938294d8da17db9109`.

This record covers target membership, dossier structure, intake invariants, and a narrow pinned Lean
API probe. The probe receives no statement or proof credit. Existing canonical `.lake` artifacts
were reused; no update, fetch, clone, dependency build, or other `.lake` mutation was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0354` | exit 0; rank 847, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0354/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0354/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0354/IntakeProbe.lean)` | exit 0; six pinned unit-interval, Lp, and basis API checks elaborated under Lean 4.29.0 |
| `rg -n '\\b(sorry|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0354 -g '*.lean'` | exit 1 as expected; no prohibited placeholder or axiom found |
| `git diff --check -- Stage1_Instances/THM-M-0354` | exit 0; no output |

Known downstream failures are intentionally open: primary-source inspection and independent review,
convention freeze, canonical target elaboration and mutations, anchor audit, obligation registry,
proof, hermetic replay, and release acceptance. They prevent theorem completion but not a truthful
planned intake.
