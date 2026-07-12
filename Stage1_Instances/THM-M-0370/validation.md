# Intake validation

Base revision: `ded29702119d0d4880db9fcf1d0a6560a89058fd`.

This validation covers manifest membership, dossier structure, JSON integrity, and a narrow pinned
Lean API probe. Because the repository record does not identify one proposition, no canonical
target, expression hash, mutation result, or proof is claimed. The canonical `.lake` symlink and
already pinned artifacts were used read-only; no update, build, fetch, or clone was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0370` | exit 0; rank 862, planned, legacy artifacts unaccepted, theorem_complete false |
| `git rev-parse HEAD` | exit 0; `ded29702119d0d4880db9fcf1d0a6560a89058fd` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0370/IntakeProbe.lean)` | exit 0; all six weighted-measure and `L^p` representation APIs elaborated |
| `python3 -m json.tool Stage1_Instances/THM-M-0370/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0370/task-dag.json` | exit 0 |
| scoped intake invariant assertions | exit 0; `intake invariant check: ok` |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0370 -g '*.lean'` | exit 1 as expected; no prohibited placeholder or axiom found |
| `git diff --check -- Stage1_Instances/THM-M-0370` | exit 0; no output |

Known downstream work remains open: pinpoint primary-source review, canonical statement
elaboration and mutation tests, discovery and obligation freezes, formal-anchor audit, proof,
hermetic replay, and release acceptance. These prevent theorem completion but do not invalidate a
truthful self-tested `planned` intake.
