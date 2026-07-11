# Intake validation

Base revision: `478034dee4145f887a572a3c645a3a2ea81bc883`.

Validation is limited to target membership, repository-standard consistency,
JSON syntax, intake invariants, and whitespace. No Lean kernel closure is
claimed because exact elaboration belongs to the statement node.

Commands run from the repository root on 2026-07-12:

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0123` | exit 0; rank 42, planned, L0/rework required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0123/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0123/task-dag.json` | exit 0 |
| scoped Python assertions over both JSON files | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0123` | exit 0; no output |

Known open downstream gates: exact Lean elaboration and environment fingerprint,
page-level source and errata audit, independent review, obligation graphs, proof
closure, trust/provenance evidence, hermetic replay, and release acceptance.
These do not invalidate the deliberately planned intake phase.
