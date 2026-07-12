# Intake validation

Validation date: `2026-07-12` (`Asia/Shanghai`). Base revision:
`e9d545372b66f73be63271b2fb408ef134d1d6f7`.

This validation covers manifest membership, dossier structure, JSON integrity, and a narrow pinned
Lean prerequisite-API probe. Because the repository record does not identify a proposition, no
canonical target, expression hash, mutation result, or proof is claimed. The canonical `.lake`
artifacts were used read-only; no update, build, fetch, or clone was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0515` | exit 0; rank 889, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0515/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0515/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0515/IntakeProbe.lean)` | exit 0; all four pinned number-field API checks elaborated under Lean 4.29.0 |
| `rg -n '\b(sorry\|admit)\b\|^[[:space:]]*axiom\b' Stage1_Instances/THM-M-0515 -g '*.lean'; test $? -eq 1` | exit 0; the search produced the expected no-match result |
| `git diff --check -- Stage1_Instances/THM-M-0515` | exit 0; no output |

Known downstream gates remain intentionally open: primary-source selection and independent review,
canonical statement elaboration and mutation tests, obligation/discovery freezes, anchor audit,
proof, hermetic replay, and release acceptance. They prevent theorem completion but do not
invalidate a truthful `planned` intake.
