# Intake validation

Validation date: `2026-07-12` (`Asia/Shanghai`). Base revision:
`5314165df54baa70993fddf08cc142a9739a74e0`.

This validation covers manifest membership, dossier structure, JSON integrity, prohibited-token
absence, and a narrow pinned Lean API probe. Because the repository record does not identify a
proposition, no canonical target, expression hash, mutation result, source acceptance, or proof is
claimed. The pre-existing canonical `.lake` artifacts were used read-only; no update, build,
fetch, or clone was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets; ranks 1..1546; all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0789` | 0 | rank 794; planned; legacy artifacts unaccepted; theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0789/instance.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0789/task-dag.json` | 0 | valid JSON |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0789/IntakeProbe.lean)` | 0 | six set-theory/filter APIs and one explicitly noncanonical candidate shape elaborated under Lean 4.29.0 |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0789 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or axiom |
| scoped Python intake assertions | 0 | item identity, planned lifecycle, open downstream DAG, empty accepted states, null canonical claim, and incomplete statuses agree |
| `git diff --check -- Stage1_Instances/THM-M-0789 .stage1-worker-selftest.json` | 0 | no whitespace errors |

Known downstream failures are intentionally open: immutable exact source selection and independent
review, canonical statement and boundary mutations, anchor audit, obligation and discovery freezes,
proof, hermetic replay, and release acceptance. They prevent theorem completion but do not
invalidate this truthful `planned` intake.
