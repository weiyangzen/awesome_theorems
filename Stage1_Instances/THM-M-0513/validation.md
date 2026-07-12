# Intake validation

Base revision: `e9d545372b66f73be63271b2fb408ef134d1d6f7`.

Validation covers manifest membership, dossier structure, JSON integrity, and a narrow pinned Lean
API probe. Since the repository record does not select an exact trace-formula identity, no
canonical target, expression hash, statement mutation result, or proof is claimed. The canonical
`.lake` artifacts were used read-only and were not updated or fetched.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0513` | exit 0; rank 887, planned, legacy artifacts unaccepted, theorem complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0513/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0513/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0513/IntakeProbe.lean)` | exit 0; all six generic pinned APIs elaborated |
| prohibited-token scan over `IntakeProbe.lean` | exit 1 from `rg` because there were no matches; scan passed |
| `git diff --check -- Stage1_Instances/THM-M-0513 .stage1-worker-selftest.json` | exit 0; no output |

## Status boundary

Known downstream gates remain open: immutable primary-source passage selection and independent
review; canonical statement elaboration and mutation tests; obligation and discovery freezes;
formal-anchor audit; proof; hermetic replay; and release acceptance. These prevent theorem
completion but do not invalidate a truthful `planned` intake.
