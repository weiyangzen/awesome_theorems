# Intake validation

Base revision: `be50e4fee4a4eab420300310f355cd6b1ed3336a`.

Validation is limited to repository/manifest consistency, dossier structure, scoped intake
invariants, a bounded pinned-source discovery search, and whitespace. No canonical Lean expression
has been selected, so no kernel elaboration or proof result is claimed. The preflight tree contained
the untracked shared `Formalizations/Lean/.lake` link/artifact; this makes the run nonrelease evidence
but does not alter the owned dossier.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0721` | exit 0; rank 578, L0/rework_required, planned, theorem_complete false |
| `rg -n 'NP\.complete\|NPComplete\|CookLevin\|Cook-Levin\|ComplexityClass\.NP' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean --glob '*.lean'` | exit 1; no matching declaration or source text (bounded local discovery only) |
| `python3 -m json.tool Stage1_Instances/THM-M-0721/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0721/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0721` | exit 0; no output |

Known downstream failures are intentionally open: primary-source theorem/definition/errata audit,
exact encodings and canonical Lean elaboration, formal-candidate audit, obligation registry, proof,
trust closure, hermetic replay, and independent review. They prevent audit and theorem completion but
do not invalidate this fail-closed `planned` intake.
