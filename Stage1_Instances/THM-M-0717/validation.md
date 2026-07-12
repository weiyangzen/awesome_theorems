# Intake validation

Base revision: `136ebf643dcdcbc42cef34e415177189578060ef`.

Validation is limited to target-set consistency, planned-dossier invariants, JSON integrity, a
narrow pinned Lean API probe, placeholder scanning, and whitespace. The pre-existing canonical
`.lake` artifacts were used read-only; no update, build, fetch, or clone was run. Because the source
record does not identify a proposition, no canonical expression, mutation result, or proof is
claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0717` | exit 0; rank 756, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0717/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0717/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0717/IntakeProbe.lean)` | exit 0; all 12 representative pinned Turing-machine API checks elaborated under Lean 4.29.0 |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0717 -g '*.lean'` | exit 1 as expected; no match |
| `git diff --check -- Stage1_Instances/THM-M-0717 .stage1-worker-selftest.json` | exit 0; no output |

Known downstream failures are intentionally open: exact source-proposition selection and
independent review, canonical statement elaboration and mutation tests, obligation/discovery
freezes, formal-anchor audit, proof, trust closure, hermetic replay, and release acceptance. They
prevent theorem completion but do not invalidate this truthful `planned` intake.
