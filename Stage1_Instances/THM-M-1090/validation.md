# Intake validation

Item: `S56-M-1090-INTAKE`  
Theorem: `THM-M-1090`  
Base revision: `45b96fd58a0e141750ae21e0ddbb3d81233b8a6a`  
Validation date: 2026-07-12 (Asia/Shanghai)

The commands below ran in this worker clone. Lean used the already materialized pinned Lake
artifacts. No `lake update`, dependency build, clone, fetch, or other `.lake` mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard validator reported 15 assurance groups, 1546 uniform-L0 Lean 4 targets, and the execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | Manifest has 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1090` | 0 | Rank 532, planned, hard anchor/wrapper lane, theorem incomplete |
| `jq -e . Stage1_Instances/THM-M-1090/intake.json Stage1_Instances/THM-M-1090/task-dag.json` | 0 | Both structured artifacts parse as JSON |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1090/IntakeProbe.lean` | 0 | Pinned imports elaborate; filtration, conditional expectation, kernel, `IsMarkovKernel`, and `condDistrib` types printed |
| `rg -n -i 'markov process\|markov property\|markov chain\|conditional.*markov\|markov.*conditional' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 0 | Matches concern Markov kernels/categories and an irreducibility comment; no declaration of a temporal Markov-process property was identified by this intake search |
| `git diff --check -- Stage1_Instances/THM-M-1090` | 0 | No whitespace errors |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |

## Result boundary

These checks self-test the assigned intake deliverable: membership, dossier structure, source/scope
crosswalk, JSON syntax, and availability of relevant Lean substrate. They do not identify or
elaborate an exact target theorem. The exact-statement gate remains open because the repository
record supplies only a property name, not a theorem with hypotheses and conclusion. Consequently
theorem completion is false, root machine debt is `M4`, and no proof or accepted receipt is claimed.

The working tree also contains the automation-provided untracked `Formalizations/Lean/.lake` link;
it was not created or modified as part of this item and makes this evidence nonrelease evidence.
