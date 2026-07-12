# Intake validation

Base revision: `c72bad9e8827ffb1ba1a585dbe346c88393b4a3f`.

This validation covers manifest membership, dossier structure, JSON integrity, and a narrow pinned
Lean API probe. Because the repository record names a method rather than one proposition, no
canonical target, expression hash, mutation result, forcing construction, or proof is claimed.
The canonical `.lake` symlink and artifacts were used read-only; no dependency mutation command
was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0780` | exit 0; rank 785, planned, legacy artifacts unaccepted, theorem_complete false |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0780/IntakeProbe.lean)` | exit 0; all six pinned first-order model-theory API checks elaborated |
| `python3 -m json.tool Stage1_Instances/THM-M-0780/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0780/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `rg -n '\\b(sorry|admit)\\b|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0780 -g '*.lean'` | exit 1 as expected; no prohibited placeholder or axiom found |
| `git diff --check -- Stage1_Instances/THM-M-0780` | exit 0; no output |

Known downstream work is intentionally open: exact source selection and independent review,
canonical statement elaboration and mutation tests, discovery and obligation freezes, formal
candidate audit, proof, hermetic replay, and release acceptance. These prevent theorem completion
but do not invalidate a truthful `planned` intake.
