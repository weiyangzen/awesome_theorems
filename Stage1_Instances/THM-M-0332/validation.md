# Intake validation

Base revision: `8014740e5a37eff82745f6fd2bc69f0ee45e67c9`.

This validation covers target membership, planned-dossier structure, JSON integrity, and a narrow
pinned Lean API probe. It does not validate a canonical holomorphic-functional-calculus statement
or a proof. The worker reused the canonical `.lake` artifacts read-only and did not update, fetch,
or otherwise mutate dependencies.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0332` | exit 0; rank 825, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0332/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0332/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0332/IntakeProbe.lean)` | exit 0; all five pinned spectrum/CFC/polynomial API checks elaborated under Lean 4.29.0 |
| `git diff --check -- Stage1_Instances/THM-M-0332` | exit 0; no output |

An initial combined validation run produced an assertion failure because this validation file had
not yet been added while the artifact-set assertion already expected it. The Lean command in that
same run still exited successfully, but the combined shell status was nonzero. After adding this
record, the complete command set above was rerun and passed.

Known downstream gates remain open: exact primary-source selection and independent review,
canonical statement elaboration and mutation tests, holomorphic-calculus candidate audit,
obligation/discovery freezes, proof, trust and provenance closure, hermetic replay, and release
acceptance. These prevent theorem completion but do not invalidate the self-tested `planned` intake.
