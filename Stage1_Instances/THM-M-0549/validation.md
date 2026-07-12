# Intake validation

Base revision: `bb527c7e738104d62e96393dc253bdc9025dbecc`.

Validation is limited to manifest membership and consistency, the planned dossier's structural
invariants, source/repository discovery, toolchain availability, JSON syntax, and whitespace. No
canonical Lean target exists yet, so the `lake env lean` result below is an environment check and
not an elaboration or kernel-proof claim.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0549` | exit 0; rank 601, no legacy slot, planned, theorem_complete false |
| `rg -n "上积\|cup product\|cupProduct" Formalizations Stage1_Instances Docs` | exit 0; repository source and adjacent discovery references found; no artifact credited |
| `cd Formalizations/Lean && lake env lean --version` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `python3 -m json.tool Stage1_Instances/THM-M-0549/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0549/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0549 .stage1-worker-selftest.json` | exit 0; no output |

The pre-existing untracked `Formalizations/Lean/.lake` link is outside this target and was not
modified. This is nonrelease worker evidence.

Known downstream failures are exact primary-source inspection, canonical statement selection and
elaboration, mutation tests, immutable source revision crosswalk, anchor audit, frozen obligation
registry, proof, hermetic replay, and independent review. They prevent any theorem-completion claim
but do not invalidate a fail-closed planned intake.
