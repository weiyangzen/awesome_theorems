# Intake validation

Base revision: `63728668acb87acd4bab7e755151dce89dc1eeb4`.

The validation surface for this intake is target membership, repository-standard consistency, the
availability of the repository-pinned Lean executable, structured planned-state invariants,
dossier references, and whitespace. No exact Lean proposition or proof declaration is introduced,
so this record makes no elaboration or kernel-proof claim. The pre-existing untracked
`Formalizations/Lean/.lake` link points to the prescribed canonical pinned artifacts; no dependency
update, build, fetch, or mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0153` | 0 | rank 652, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `python3 -m json.tool` on `intake.json` and `task-dag.json` | 0 | both structured artifacts are valid JSON |
| scoped planned-instance assertions | 0 | item/target/rank/lifecycle/root-state/task-chain and no-accepted-state invariants pass |
| scoped dossier reference checks | 0 | all declared public merge targets and task dependencies exist |
| forbidden proof-escape scan under the owned path | 0 | no Lean proof-escape marker or placeholder file was found |
| `git diff --check -- Stage1_Instances/THM-M-0153 .stage1-worker-selftest.json` | 0 | no whitespace errors |

Known open gates are the inspected and immutable primary-source crosswalk, exact Lean target and
environment fingerprint, statement mutations, immutable anchor audit, frozen obligation registry,
proof, trust and provenance closure, readable reconstruction, hermetic release replay, and
independent verification. They prevent audit and theorem completion but do not invalidate this
fail-closed `planned` intake.
