# Intake validation

Base revision: `16187d91397de4edab8cb93140166f634baa0c02`.

Validation is intentionally limited to target-set consistency, dossier syntax, scoped intake
invariants, and whitespace. The metadata does not identify one proposition, so a Lean elaboration
would validate an invented or borrowed substitute. No kernel, source-review, audit, or
theorem-completion result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0666` | exit 0; rank 710, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0666/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0666/task-dag.json` | exit 0 |
| scoped Python intake assertions over the instance, DAG, and owned file set | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0666` | exit 0; no output |

Known downstream failures: a primary-source theorem and variant have not been selected; the
relationship to the duplicate-name `THM-M-0465` target is unresolved; the canonical human claim,
domains, binders, hypotheses, conclusion, profiles, Lean expression, and fingerprints are open;
source review, mutation tests, formal-candidate audit, obligation registry, proof, hermetic replay,
and independent verification remain open. These failures prevent every later phase but do not
invalidate a truthful `planned` intake.
