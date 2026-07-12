# Intake validation

Base revision: `32404187d6cee70b44ae90adf8d0d765752e5149`.

This validation covers target membership, dossier structure, JSON integrity, scoped intake
invariants, and a narrow pinned Lean API probe. Since the repository supplies no exact property or
source proposition, no canonical expression, mutation test, supercompactness definition, or proof
is claimed. The canonical `.lake` artifacts were consumed read-only; no update, build, clone, or
fetch was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0790` | exit 0; rank 795, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0790/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0790/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0790/IntakeProbe.lean)` | exit 0; all six pinned encoding-ingredient checks elaborated under Lean 4.29.0 |
| `rg -n '\b(sorry\|admit)\b\|^[[:space:]]*axiom\b' Stage1_Instances/THM-M-0790 -g '*.lean'` | exit 1 as expected for no matches; no prohibited placeholder or axiom found |
| `git diff --check -- Stage1_Instances/THM-M-0790 .stage1-worker-selftest.json` | exit 0; no output |

Known downstream gates intentionally remain open: exact primary-source selection and independent
review, selection of one property and definition variant, canonical statement elaboration and
mutation tests, discovery and obligation freezes, anchor audit, proof, hermetic replay, and release
acceptance. They prevent theorem completion but do not invalidate a truthful `planned` intake.
