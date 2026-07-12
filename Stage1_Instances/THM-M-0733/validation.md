# Intake validation

Base revision: `f12b1ccbda307337d488a2993eddbf883b722be6`.

This validation covers manifest membership, dossier structure, JSON integrity, prohibited-token
absence, and a narrow pinned Lean API probe. Because the repository record does not identify a
proposition, no canonical target, expression hash, mutation result, source-proof status, or theorem
proof is claimed. The pre-existing canonical `.lake` artifacts were used read-only; no update,
build, fetch, or clone was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets validated |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0733` | exit 0; rank 770, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0733/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0733/task-dag.json` | exit 0 |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0733/IntakeProbe.lean)` | exit 0; six pinned finite-function/cardinality/computability API checks elaborated under Lean 4.29.0 |
| prohibited-token scan over the target's Lean files | exit 1 as expected for no matches; no placeholder or axiom token found |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0733` | exit 0; no output |

An initial probe referenced nonexistent `Equiv.card_congr` and exited 1. It was corrected to the
available `Fintype.card_fun`; the table records the final successful self-test. No theorem claim
depended on either API check.

Known downstream gates remain intentionally open: pinpoint source selection and independent review,
canonical statement elaboration and mutations, discovery and obligation freezes, formal anchor
audit, proof, hermetic replay, and release acceptance. They prevent theorem completion but do not
invalidate this truthful `planned` intake.
