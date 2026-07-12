# Intake validation

Base revision: `347a3f61a73c2987a5e0b2b9bed8c07961d8b1a5`.

Validation covers manifest consistency, dossier structure, scoped intake invariants, and a narrow
Lean discovery probe against the existing pinned artifacts. It does not establish exact statement
identity or proof acceptance. The pre-existing untracked `Formalizations/Lean/.lake` link/artifact
was not created or modified by this task and makes this nonrelease worker evidence.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0673` | exit 0; rank 717, L0/rework_required, planned, theorem_complete false |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0673/IntakeProbe.lean` | exit 0; printed the expected sentence satisfaction biconditional for `FirstOrder.Language.Ultraproduct.sentence_realize` |
| `python3 -m json.tool Stage1_Instances/THM-M-0673/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0673/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0673` | exit 0; no output |

Known downstream failures: primary-source pinpointing and review, canonical expression hashing,
statement mutations and checked alternate transports, obligation registry, provenance/trust audit,
proof acceptance, hermetic replay, readable reconstruction, and independent verification remain
open. They prevent audit and theorem completion but do not invalidate this planned intake.
