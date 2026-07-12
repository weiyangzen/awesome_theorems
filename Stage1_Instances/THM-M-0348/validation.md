# Intake validation

Base revision: `bd0d227173ac95971603f633607751754850337e`.

This record covers manifest membership, dossier structure, JSON integrity, and a narrow pinned Lean
API probe. Because the repository record does not identify a proposition, no canonical target,
expression hash, mutation result, axiom report, or proof is claimed. The existing canonical `.lake`
artifacts were reused read-only and were not updated or fetched.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0348` | exit 0; rank 841, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0348/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0348/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0348/IntakeProbe.lean)` | exit 0; all five pinned Fourier/Cesaro/Laurent API checks elaborated under Lean 4.29.0 |
| `git diff --check -- Stage1_Instances/THM-M-0348` | exit 0; no output |

Known downstream failures are intentionally open: independently reviewed exact source selection,
canonical statement elaboration and mutation tests, obligation and discovery freezes, anchor audit,
proof, hermetic replay, and release acceptance. They prevent theorem completion but do not invalidate
a truthful `planned` intake.
