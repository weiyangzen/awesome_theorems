# Intake validation

Base revision: `62079b9309b9fd52b92c67032eb6543ea54a0c3f` (2026-07-12).

Commands were run from the repository root on 2026-07-12 (Asia/Shanghai). Final post-edit
results are recorded below.

| Command | Exit | Result |
|---|---:|---|
| `python3 -m json.tool Stage1_Instances/THM-M-1095/intake.json >/dev/null` | 0 | Intake JSON parsed |
| `python3 -m json.tool Stage1_Instances/THM-M-1095/task-dag.json >/dev/null` | 0 | Task DAG JSON parsed |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed: 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | Passed: 1546 unique targets with ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1095` | 0 | Confirmed rank 535, planned lifecycle, L0/rework-required baseline, and theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-1095` | 0 | No whitespace errors |
| `rg -n '\\bsorry\\b|\\baxiom\\b|placeholder|fake result' Stage1_Instances/THM-M-1095/{README.md,intake.json,scope-map.md,source-statement-crosswalk.md,task-dag.json}` | 1 | No forbidden proof construct or result wording found; ripgrep exit 1 means no matches |

No `lake env lean` command was run because the source statement does not identify a proposition,
so there is no truthful Lean expression to elaborate. Inventing one merely to obtain a green kernel
check would violate the exact-statement gate. This is the recorded blocker for the dependent
statement phase, not a claim that Lean validation passed.

These checks self-test only the assigned intake deliverable: manifest membership, dossier syntax,
scope/crosswalk presence, and the open planned DAG. They provide no source acceptance, elaboration,
kernel proof, or theorem-completion evidence. The untracked `Formalizations/Lean/.lake` entry was
present before this work and was neither modified nor used as completion evidence.
