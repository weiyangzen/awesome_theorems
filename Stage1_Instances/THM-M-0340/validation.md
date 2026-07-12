# Intake validation

Validation date: `2026-07-12` (`Asia/Shanghai`). Base revision:
`3d8dd27e4ff1200a2d9c8daaa9cae8072eca6241`.

This validation covers manifest membership, dossier structure, JSON integrity, absence of Lean
placeholders, and a narrow pinned Lean API probe. Because the repository record does not identify
one proposition, no canonical target, expression hash, mutation result, source acceptance, or proof
is claimed. The pre-existing canonical `.lake` link and artifacts were used read-only; no update,
build, fetch, or clone was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets; ranks 1..1546; all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0340` | 0 | rank 833; planned; legacy artifacts unaccepted; theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0340/instance.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0340/task-dag.json` | 0 | valid JSON |
| scoped Python intake assertions | 0 | theorem/item identity, planned lifecycle, open canonical target, empty accepted states, exact downstream DAG, and owned artifacts agree |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0340/IntakeProbe.lean)` | 0 | nine pinned equidecomposition, Euclidean, ball/sphere, and isometry API checks elaborated under Lean 4.29.0 |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0340 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or axiom in Lean source |
| `git diff --check -- Stage1_Instances/THM-M-0340` | 0 | no whitespace errors |

Known downstream failures are intentionally open: exact primary-source selection and independent
review; canonical statement elaboration, fingerprint, transports, and mutations; obligation and
discovery freezes; anchor audit; proof; hermetic and independent replay; and release acceptance.
They prevent theorem completion but do not invalidate this truthful `planned` intake.

