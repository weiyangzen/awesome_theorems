# Intake validation

Base revision: `136ebf643dcdcbc42cef34e415177189578060ef`.

This validation covers manifest membership, dossier structure, JSON integrity, and a narrow pinned
Lean API probe. Because the repository record does not define recursive enumerability or the exact
Diophantine encoding, no canonical target, expression hash, mutation result, or proof is claimed.
The existing canonical `.lake` artifacts were used read-only and were not modified.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0714` | exit 0; rank 753, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0714/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0714/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0714/IntakeProbe.lean)` | exit 0; all seven pinned computability/Diophantine API checks elaborated under Lean 4.29.0 |
| `git diff --check -- Stage1_Instances/THM-M-0714` | exit 0; no output |

Known downstream failures are intentionally open: primary-source identification and independent
review, exact statement elaboration and mutation tests, obligation and discovery freezes, complete
formal-anchor audit, proof, hermetic replay, and release acceptance. They prevent theorem completion
but do not invalidate a truthful `planned` intake.
