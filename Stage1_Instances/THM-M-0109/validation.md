# Intake validation

Base revision: `a8d6489fd935cd71fa4499f2f3f5b051998203f4`.

Validation is limited to target membership, rev-5.6 repository consistency,
structured dossier syntax/invariants, and scoped whitespace checks. No Lean
kernel result is claimed because the exact proposition is unresolved.

Commands run from the repository root on 2026-07-12:

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0109` | 0 | rank 33, `planned`, `L0`, rework required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0109/instance.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0109/task-dag.json` | 0 | valid JSON |
| scoped Python assertions over both JSON records and the owned file set | 0 | `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0109` | 0 | no whitespace errors |

Known downstream failure: the source name and gloss do not determine one exact
proposition. The retry condition is an authoritative, inspectable source
locator resolving that conflict. This is recorded as statement/source debt and
does not prevent the planned intake itself from being self-tested.
