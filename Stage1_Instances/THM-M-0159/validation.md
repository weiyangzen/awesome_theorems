# Intake validation

Base revision: `c8bb1d8f046a4b2816eb059edc201b88d2063f42`.

Validation is limited to target-set consistency, the pinned Lean executable, structured
`planned`-state invariants, dossier-local references, forbidden proof escapes, and whitespace. This
intake introduces no canonical Lean proposition or proof declaration, so no elaboration or kernel
proof result is claimed. The pre-existing untracked `Formalizations/Lean/.lake` link is the
prescribed reuse of canonical pinned artifacts; it was not modified.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0159` | 0 | rank 658, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `python3 -m json.tool` on `instance.json` and `task-dag.json` | 0 | both structured artifacts are valid JSON |
| scoped planned-instance and task-chain assertions | 0 | target/item/rank/lifecycle/root vector, no-accepted-state, ordered dependency chain, and declared-artifact invariants pass |
| scoped dossier reference and forbidden proof-escape checks | 0 | every dossier file identifies this target or item; no Lean proof-escape marker occurs under the owned path |
| `git diff --check -- Stage1_Instances/THM-M-0159 .stage1-worker-selftest.json` | 0 | no whitespace errors |

Known downstream open gates are immutable source inspection and independent review, exact Lean
statement elaboration and mutation testing, anchor audit, frozen obligation graphs, proof,
provenance and trust closure, readable reconstruction, hermetic replay, and independent release
verification. They prevent audit and theorem completion but do not invalidate this fail-closed
planned intake.
