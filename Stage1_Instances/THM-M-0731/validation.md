# Intake validation

Base revision: `d19d83e12b57432e75cbb1c35f4577d5b0645cf9`.

This validation covers manifest membership, dossier structure, JSON integrity, prohibited-token
absence, and a narrow pinned Lean API probe. Because the repository record does not identify a
proposition, no canonical target, expression hash, mutation result, source proof, or theorem proof
is claimed. The pre-existing canonical `.lake` artifacts were used read-only; no update, build,
fetch, or clone was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0731` | exit 0; rank 768, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0731/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0731/task-dag.json` | exit 0 |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0731/IntakeProbe.lean)` | exit 0; six pinned probability/computability API checks elaborated under Lean 4.29.0 |
| prohibited-token scan over the target's Lean files | exit 1 as expected for no matches; no placeholder or axiom token found |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0731` | exit 0; no output |

Known downstream gates remain intentionally open: pinpoint source selection and independent review,
canonical statement elaboration and mutations, discovery and obligation freezes, formal anchor
audit, proof, hermetic replay, and release acceptance. They prevent theorem completion but do not
invalidate this truthful `planned` intake.
