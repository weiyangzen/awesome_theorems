# Intake validation

Base revision: `2ff2721a0184cf5f856054cb7d46b10dbc703f5a`.

Validation is limited to target membership, dossier structure, scoped intake invariants, JSON
syntax, and whitespace. There is deliberately no canonical Lean expression yet: running
`lake env lean` against an invented model equivalence would validate a substituted theorem, so no
kernel result is claimed at intake. The pre-existing untracked `Formalizations/Lean/.lake` is the
automation clone's link to canonical pinned artifacts and was not created or mutated here.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0706` | exit 0; rank 747, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0706/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0706/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions (manifest rank/baseline, dossier identity/lifecycle/debt boundary, exact downstream DAG, no accepted state) | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0706 .stage1-worker-selftest.json` | exit 0; no output |

Known downstream failures: repository sources conflict on whether the target is a formal
equivalence family or the informal thesis; a primary-source theorem/page and errata audit, exact
model pair, domains, partiality and encoding conventions, canonical Lean elaboration, anchor
audit, obligation registry, proof, hermetic replay, and independent review remain open. These
failures block theorem completion but do not invalidate this fail-closed planned intake.
