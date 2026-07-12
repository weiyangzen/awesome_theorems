# Intake validation

Base revision: `061a312aab9d8774275e6b9293e58cabde5fe6a3`.

Validation is intentionally limited to manifest consistency, the available pinned Lean executable,
dossier structure, scoped intake invariants, JSON syntax, and whitespace. The source phrase does
not determine a canonical Lean proposition, so elaborating an invented expression would be false
evidence. No `.lake` content was fetched or mutated, and no kernel theorem result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1109` | exit 0; rank 549, no legacy slot, planned, L0/rework_required, theorem_complete false |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `python3 -m json.tool Stage1_Instances/THM-M-1109/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1109/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; exact file set, IDs, manifest fields, planned lifecycle, empty accepted states, false completion flags, linear open downstream dependencies, and newline invariants verified |
| `git diff --check -- Stage1_Instances/THM-M-1109 .stage1-worker-selftest.json` | exit 0; no output |

Known downstream failures are unique primary-source proposition selection, exact source review,
canonical Lean elaboration and statement mutations, anchor audit, frozen obligation graphs, proof,
hermetic replay, and independent review. They prevent theorem completion but do not invalidate a
truthful fail-closed `planned` intake.
