# Intake validation

Base revision: `ded29702119d0d4880db9fcf1d0a6560a89058fd`.

This validation covers manifest membership, dossier structure, JSON integrity, and a narrow pinned
Lean API probe. Because the repository record does not identify a proposition, no canonical target,
expression hash, mutation result, proof, or formal-anchor closure is claimed. The shared canonical
`.lake` symlink was used read-only and no update, build, fetch, or clone was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0369` | exit 0; rank 861, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0369/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0369/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0369/IntakeProbe.lean)` | exit 0; all six pinned analysis API checks elaborated under Lean 4.29.0 |
| `rg -n '\b(sorry\|admit)\b\|^[[:space:]]*axiom\b' Stage1_Instances/THM-M-0369 -g '*.lean'` | exit 1 as expected for no matches; no prohibited placeholder or axiom found |
| `git diff --check -- Stage1_Instances/THM-M-0369` | exit 0; no output |

Known downstream failures are intentionally open: pinpoint primary-source selection and independent
review, canonical statement elaboration and mutation tests, discovery and obligation freezes,
formal-anchor audit, proof, hermetic replay, and release acceptance. They prevent theorem completion
but do not invalidate a truthful `planned` intake.
