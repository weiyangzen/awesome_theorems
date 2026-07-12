# Intake validation

Base revision: `60fe286fb6a79de4164adae42c8b29610e7f5cde`.

Validation is limited to repository/manifest consistency, dossier structure, scoped intake
invariants, and whitespace. No canonical Lean expression has been selected, so a Lean elaboration
command would validate an invented or abstract substitute rather than this theorem. No kernel
result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0363` | exit 0; rank 681, no legacy slot, L0/rework_required, planned, theorem_complete false |
| `rg -n -i 'BMO|bounded mean oscillation|Hardy space' Formalizations Stage1_Instances Docs` | exit 0; repository prose hits but no target-specific Lean artifact; generic false-positive code hits excluded |
| `find Formalizations/Lean/.lake/packages/mathlib/Mathlib -type f \| rg -i 'Hardy\|BMO\|MeanOscillation'` | exit 0 due unrelated path-name matches; no BMO/real Hardy-space module identified |
| `curl -L --max-time 20 -s 'https://api.crossref.org/works?query.title=Characterizations%20of%20bounded%20mean%20oscillation&query.author=Fefferman&rows=5'` | exit 0; DOI metadata identifies Fefferman, 1971, volume 77 issue 4, pages 587-588, DOI `10.1090/s0002-9904-1971-12763-5` |
| `python3 -m json.tool Stage1_Instances/THM-M-0363/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0363/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0363` | exit 0; no output |

Known downstream failures are exact primary-text inspection, source assumptions/errata, canonical
Lean elaboration, immutable anchor audit, obligation registry, proof, hermetic replay, and
independent review. They prevent theorem completion but do not invalidate this fail-closed planned
intake.
