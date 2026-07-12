# Intake validation

Base revision: `6225a82e61b00264db6b5520dbe8304213d97f4a`.

This validation covers manifest membership, dossier structure, JSON integrity, and a narrow pinned
Lean prerequisite-API probe. Because the repository gloss is under-specified and false on its
unrestricted reading, no canonical target, expression hash, mutation result, human theorem, or
machine proof is claimed. The canonical `.lake` artifacts were used read-only and were not
modified.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0683` | exit 0; rank 724, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0683/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0683/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0683/IntakeProbe.lean)` | exit 0; all five pinned encoding/beta-function API checks elaborated under Lean 4.29.0 |
| `git diff --check -- Stage1_Instances/THM-M-0683` | exit 0; no output |

Known downstream failures are intentionally open: exact primary-source selection and independent
review, canonical statement elaboration and mutations, obligation/discovery freezes, immutable
formal-anchor audit, proof, hermetic replay, and release acceptance. They prevent theorem
completion but do not invalidate a truthful `planned` intake.
