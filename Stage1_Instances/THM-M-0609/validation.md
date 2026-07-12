# Intake validation

Base revision: `162f31e26f99fc08e308d576b8fb1b6f18a338c6`.

Validation is limited to repository/manifest consistency, dossier structure, scoped intake
invariants, and whitespace. The worktree already contained the untracked shared
`Formalizations/Lean/.lake` link; it was not modified. Because the repository phrase does not yet
determine a canonical proposition, running `lake env lean` would elaborate a substituted target;
no Lean kernel result is claimed for this intake.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0609` | exit 0; rank 646, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0609/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0609/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0609` | exit 0; no output |
| `rg -n -i 'sorry|admit|axiom|placeholder|fake result' Stage1_Instances/THM-M-0609` | exit 1; no prohibited token found (expected ripgrep no-match status) |

Known downstream failures: selection and exact inspection of one primary-source proposition,
independent source review, canonical Lean elaboration and mutation tests, anchor audit, obligation
registry, proof, hermetic replay, and independent validation remain open. The generic source title
is an actionable statement-phase blocker. These failures prevent audit and theorem completion but
do not invalidate this fail-closed planned intake.
