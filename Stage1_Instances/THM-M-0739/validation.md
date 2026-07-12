# Intake validation

Base revision: `91055abb3f5bee7f79323bc9cbefa7f2a8145f1f`.

This validation covers target membership, dossier structure, JSON integrity, and a narrow pinned
Lean API probe. Because the repository record does not identify a proposition, no canonical target,
expression hash, mutation result, or proof is claimed. The canonical `.lake` artifacts were used
read-only; no update, build, clone, or fetch was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0739` | exit 0; rank 775, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0739/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0739/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0739/IntakeProbe.lean)` | exit 0; all seven finite Boolean-function API/type checks elaborated under pinned Lean 4.29.0 |
| placeholder/axiom scan of owned Lean files | exit 0; no prohibited token found |
| `git diff --check -- Stage1_Instances/THM-M-0739 .stage1-worker-selftest.json` | exit 0; no output |

Known downstream failures are intentionally open: primary-source selection and independent review;
circuit-model, function-family, resource-bound, and exact inequality selection; canonical statement
elaboration and mutation tests; obligation and discovery freezes; formal-anchor audit; proof;
hermetic replay; and release acceptance. They prevent theorem completion but do not invalidate a
truthful `planned` intake.
