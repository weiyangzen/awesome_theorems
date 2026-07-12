# Intake validation

Validation date: `2026-07-12` (`Asia/Shanghai`). Base revision:
`e9d545372b66f73be63271b2fb408ef134d1d6f7`.

This validation covers manifest membership, dossier structure, JSON integrity, placeholder hygiene,
and a narrow pinned Lean API probe. Because the repository record does not identify one
proposition, no canonical target, expression hash, mutation result, source acceptance, or proof is
claimed. `Formalizations/Lean/.lake` is an inherited untracked link to the canonical pinned
artifacts; it was used read-only and was not modified. No update, build, clone, or fetch was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0514` | exit 0; rank 888, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0514/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0514/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; membership, planned lifecycle, empty accepted state, root vector, null target, and six open downstream DAG nodes agree |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0514/IntakeProbe.lean)` | exit 0; all five nearby pinned APIs elaborated under Lean 4.29.0 |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0514 -g '*.lean'` | exit 1 as expected; no prohibited placeholder or axiom found |
| `git diff --check -- Stage1_Instances/THM-M-0514 .stage1-worker-selftest.json` | exit 0; no output |

Known downstream failures are intentionally open: primary-source selection and independent review,
canonical statement elaboration and mutations, obligation and discovery freezes, formal anchor
audit, proof, hermetic replay, and release acceptance. They prevent theorem completion but do not
invalidate this truthful `planned` intake.
