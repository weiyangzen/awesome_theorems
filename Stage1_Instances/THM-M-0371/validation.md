# Intake validation

Base revision: `b8a117cd19ae3b30b59087d7bc9c8071ee7212ab`.

This validation covers target membership, dossier structure, JSON integrity, and a narrow pinned
Lean API probe. Because the repository record does not identify one proposition, no canonical
target, expression hash, mutation result, proof, or formal-anchor closure is claimed. The canonical
`.lake` symlink and pinned artifacts were used read-only; no update, build, fetch, or clone was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0371` | exit 0; rank 863, planned, legacy artifacts unaccepted, theorem_complete false |
| `git rev-parse HEAD` | exit 0; `b8a117cd19ae3b30b59087d7bc9c8071ee7212ab` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0371/IntakeProbe.lean)` | exit 0; all six weighted-measure and `L^p` representation APIs elaborated |
| `python3 -m json.tool Stage1_Instances/THM-M-0371/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0371/task-dag.json` | exit 0; valid JSON |
| scoped intake invariant assertions | exit 0; `intake invariant check: ok` |
| `rg -n '\\b(sorry|admit)\\b|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0371 -g '*.lean'` | exit 1 as expected; no prohibited placeholder or axiom found |
| `git diff --check -- Stage1_Instances/THM-M-0371` | exit 0; no output |

Known downstream work remains open: pinpoint primary-source inspection and independent review,
canonical statement elaboration and mutation tests, discovery and obligation freezes, immutable
formal-anchor audit, proof, hermetic replay, and release acceptance. These prevent theorem
completion but do not invalidate a truthful self-tested `planned` intake.
