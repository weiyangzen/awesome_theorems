# Intake validation

Base revision: `fc8e70dc8b3df070bf824de575d4a369542a621f`.

Validation is intentionally limited to manifest membership, the rev-5.6 structural baseline, JSON
syntax, planned-state invariants, owned-path containment, and whitespace. There is no exact Lean
target in this intake: running an unrelated elaboration would be false evidence. Source selection,
canonical Lean elaboration, environment fingerprinting, and statement mutation tests belong to the
dependent statement node.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0330` | exit 0; rank 823, lane `hard_statement_first_partial_verification`, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0330/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0330/task-dag.json` | exit 0; valid JSON |
| scoped Python assertions over identity/rank, lifecycle, false terminal flags, empty accepted state, exact owned-file set, and the six-node open dependency chain | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0330` | exit 0; no output |

Known downstream failures are explicit: no pinpoint primary-source/errata review, selected theorem
variant, elaborated expression or expression hash, foundation and import fingerprint, statement
mutation suite, formal-anchor audit, obligation registry, proof closure, hermetic replay, or
independent acceptance exists. These failures keep both audit and theorem completion false.
