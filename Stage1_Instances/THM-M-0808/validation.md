# Intake validation

Base revision: `8f8873f36acbc62e9b41b932a8bb65bf355c8ccf`.

This validation covers manifest membership, dossier structure, JSON integrity, and a narrow pinned
Lean API probe. Because the repository record does not identify a proposition, no canonical target,
expression hash, mutation result, source acceptance, or proof is claimed. The pre-existing shared
`.lake` symlink and canonical pinned artifacts were used read-only and were not modified.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0808` | exit 0; rank 811, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0808/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0808/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0808/IntakeProbe.lean)` | exit 0; five pinned descriptive-set-theory API checks elaborated under Lean 4.29.0 |
| `rg -n '\b(sorry\|admit)\b\|^[[:space:]]*axiom\b' Stage1_Instances/THM-M-0808 -g '*.lean'` | exit 1, expected no-match result; no prohibited placeholder or axiom in the Lean probe |
| `git diff --check -- Stage1_Instances/THM-M-0808` | exit 0; no output |

Known downstream failures are intentionally open: exact source selection and independent review,
canonical statement elaboration and mutation tests, foundation and pointclass decisions, discovery
and obligation freezes, formal-anchor audit, proof, hermetic replay, and release acceptance. They
prevent theorem completion but do not invalidate a truthful `planned` intake.
