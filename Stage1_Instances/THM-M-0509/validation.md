# Intake validation

Base revision: `3f994388953e417edafd54b069ab45d648619698`.

This validation covers manifest membership, dossier structure, JSON integrity, and a narrow pinned
Lean API probe. It does not claim a canonical target, expression hash, source acceptance, mutation
result, or proof. The canonical `.lake` artifacts were used read-only; no update, build, fetch, or
clone was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0509` | exit 0; rank 883, planned, legacy artifacts unaccepted, theorem_complete false |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0509/IntakeProbe.lean)` | exit 0; all five pinned number-theory/filter API checks elaborated under Lean 4.29.0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0509/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0509/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `rg -n '\b(sorry\|admit)\b\|^[[:space:]]*axiom\b' Stage1_Instances/THM-M-0509 -g '*.lean'` | exit 1, expected no-match result; no prohibited placeholder or axiom found |
| `git diff --check -- Stage1_Instances/THM-M-0509` | exit 0; no output |

Known downstream work remains intentionally open: primary-source inspection and independent review,
canonical statement elaboration and mutation tests, discovery and obligation freezes, anchor audit,
proof, hermetic replay, and release acceptance. These prevent theorem completion but do not
invalidate a truthful `planned` intake.
