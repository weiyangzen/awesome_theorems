# Intake validation

Base revision: `1a30b84c1f86a2bbbf08b36f9afd06912b8f6c06`.

Validation is limited to target membership, standard consistency, dossier JSON syntax, planned-state
invariants, owned-file scope, and whitespace. This intake deliberately does not claim a Lean kernel
check because selecting and elaborating the exact formal root belongs to the dependent statement node.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0001` | exit 0; rank 96, lane `hard_mathlib_anchor_and_wrapper`, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0001/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0001/task-dag.json` | exit 0 |
| scoped Python assertions over theorem/item identity, planned lifecycle, empty accepted states, six open downstream tasks, and the owned file set | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0001` | exit 0; no output |

Known downstream failures: no primary-source pinpoint/errata review, elaborated target, expression
hash, environment fingerprint, mutation suite, frozen obligation registry, anchor provenance audit,
proof closure, hermetic replay, or independent acceptance exists. A legacy Lean wrapper was inspected
only to set an honest scope boundary. These failures keep all theorem and audit completion claims false.
