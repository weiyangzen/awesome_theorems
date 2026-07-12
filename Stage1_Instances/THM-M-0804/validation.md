# Intake validation

Validation date: `2026-07-12` (`Asia/Shanghai`). Base revision:
`5278269d3ea693eba5c4c533ad3fe61693da0620`.

This validation covers manifest membership, dossier structure, JSON integrity, a bounded mathlib
name search, and a narrow pinned Lean API probe. Because the repository record does not identify a
proposition, no canonical target, expression hash, mutation result, or proof is claimed. The shared
canonical `.lake` symlink was used read-only; no update, build, clone, or fetch was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0804` | exit 0; rank 807, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0804/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0804/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0804/IntakeProbe.lean)` | exit 0; all five pinned ZFC API checks elaborated under Lean 4.29.0 |
| `rg -n -i 'core model\|inner model\|premouse\|extender model' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` followed by an empty-result assertion | exits 1 then 0 as expected; no matching mathlib source line |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0804 -g '*.lean'` under shell negation | search exit 1, negated command exit 0; no prohibited placeholder or axiom |
| `git diff --check -- Stage1_Instances/THM-M-0804` | exit 0; no output |

Known downstream work is intentionally open: exact source selection and independent review,
canonical statement elaboration and mutation tests, obligation and discovery freezes, formal-anchor
audit, proof, hermetic replay, and release acceptance. These prevent theorem completion but do not
invalidate a truthful `planned` intake.
