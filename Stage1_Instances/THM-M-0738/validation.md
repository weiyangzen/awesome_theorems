# Intake validation

Base revision: `3159849a5319960dea505779c7c20894ea30487c`.

This validation covers manifest membership, dossier structure, JSON integrity, prohibited-token
absence, and a narrow pinned Lean API probe. Because the repository record does not identify a
proposition, no canonical target, expression hash, mutation result, source-proof status, or theorem
proof is claimed. The pre-existing canonical `.lake` artifacts were used read-only; no dependency
update, build, fetch, or clone was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets validated |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0738` | exit 0; rank 774, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0738/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0738/task-dag.json` | exit 0; valid JSON |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0738/IntakeProbe.lean)` | exit 0; five pinned finite-function/cardinality/computability API checks elaborated under Lean 4.29.0 |
| `! rg -n '\b(sorry|admit)\b\|^[[:space:]]*axiom\b' Stage1_Instances/THM-M-0738 -g '*.lean'` | exit 0 after negating expected no-match exit; no prohibited placeholder or axiom found |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` for identity, planned lifecycle, rank, absent canonical claim, empty accepted states, open DAG, and artifact inventory |
| `git diff --check -- Stage1_Instances/THM-M-0738` | exit 0; no output |

Known downstream gates remain intentionally open: pinpoint source selection and independent review,
canonical statement elaboration and mutations, discovery and obligation freezes, formal anchor
audit, proof, hermetic replay, and release acceptance. They prevent theorem completion but do not
invalidate a truthful `planned` intake.
