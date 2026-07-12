# Intake validation

Base revision: `6f601f70dc531aafc2c0e73ea51db67cebeb3ad9`.

This validation covers manifest membership, dossier structure, JSON integrity, and a narrow pinned
Lean API probe. Because the repository record does not identify a unique estimate, no canonical
target, expression hash, mutation result, Strichartz theorem, or proof is claimed. The canonical
`.lake` symlink and artifacts were used read-only and were not modified.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0381` | exit 0; rank 869, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0381/instance.json` | exit 0; syntactically valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0381/task-dag.json` | exit 0; syntactically valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0381/IntakeProbe.lean)` | exit 0; seven pinned analytic APIs and one time-section encoding elaborated under Lean 4.29.0 |
| `rg -n '\\b(sorry|admit)\\b|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0381 -g '*.lean'` | exit 1 as expected for no matches; no prohibited placeholder or axiom found |
| `git diff --check -- Stage1_Instances/THM-M-0381` | exit 0; no output |

Known downstream failures are intentionally open: exact primary-source selection and independent
review; equation, exponent, norm, endpoint, and boundary decisions; canonical statement elaboration
and mutation tests; obligation and discovery freezes; formal-anchor audit; proof; hermetic replay;
and release acceptance. They prevent theorem completion but do not invalidate a truthful `planned`
intake.
