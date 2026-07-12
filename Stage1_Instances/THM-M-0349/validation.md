# Intake validation

Base revision: `c9694802ae049af37973e49a65f11b833135333f`.

This validation covers target membership, dossier structure, scoped intake invariants, and a narrow
pinned Lean API probe. No canonical proposition has been selected, so the probe receives no
statement or proof credit. The canonical `.lake` artifacts were reused read-only; no dependency
update, fetch, clone, or build was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0349` | exit 0; rank 842, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0349/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0349/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0349/IntakeProbe.lean)` | exit 0; six pinned circle, Haar, and Lp API checks elaborated under Lean 4.29.0 |
| `rg -n '\\b(sorry|admit)\\b|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0349 -g '*.lean'` | exit 1 as expected; no prohibited placeholder or axiom found |
| `git diff --check -- Stage1_Instances/THM-M-0349` | exit 0; no output |

Known downstream failures remain intentionally open: exact primary-source inspection and independent
review, convention freeze, canonical Lean elaboration and mutation tests, immutable anchor audit,
obligation registry, proof, hermetic replay, and release acceptance. They prevent theorem completion
but do not invalidate this truthful `planned` intake.

The later statement-phase evidence is recorded separately in `statement-validation.md`. It
supersedes the intake-only claims that convention freeze and canonical elaboration remain open, but
does not alter the intake receipt or grant proof credit.
