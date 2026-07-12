# Intake validation

Base revision: `d30ab383279f10fe53d90d3c5b5421638c550b25`.

Validation is limited to manifest consistency, dossier structure, the literal source boundary,
scoped intake invariants, and whitespace. The metadata does not specify a proposition, so creating
or elaborating a generic Lean proposition would be a substituted target rather than kernel evidence.
The pre-existing untracked `Formalizations/Lean/.lake` symlink is shared worker-clone infrastructure;
it was not modified.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0566` | exit 0; rank 614, L0/rework_required, planned, theorem_complete false |
| `rg -n 'Pontryagin\|Pontrjagin\|庞特里亚金\|0566' .` with generated target projections and `.lake` excluded | exit 0; theorem metadata, generic mentions, and adjacent dossier references found; no target-specific Lean artifact found |
| `python3 -m json.tool Stage1_Instances/THM-M-0566/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0566/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0566` | exit 0; no output |

Known downstream failures: a single source-located proposition, exact edition/theorem/page and
errata, source date reconciliation, base and bundle hypotheses, coefficient/index/normalization
conventions, canonical Lean elaboration, anchor audit, obligation registry, proof, hermetic replay,
and independent review remain open. They prevent theorem completion but do not invalidate this
fail-closed planned intake.
