# Intake validation

Item: `S56-M-1091-INTAKE`  
Theorem: `THM-M-1091`  
Base revision: `62079b9309b9fd52b92c67032eb6543ea54a0c3f`  
Validation date: 2026-07-12 (Asia/Shanghai)

The commands below ran in this worker clone. Lean used the automation-provided link to already
materialized pinned Lake artifacts. No `lake update`, build, dependency clone/fetch, or other
`.lake` mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard validator reported 15 assurance groups, 1546 uniform-L0 Lean 4 targets, and the execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | Manifest has 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1091` | 0 | Rank 533, planned, hard mathlib anchor/wrapper lane, theorem incomplete |
| `jq -e . Stage1_Instances/THM-M-1091/intake.json Stage1_Instances/THM-M-1091/task-dag.json` | 0 | Both structured artifacts parse as JSON |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1091/IntakeProbe.lean` | 0 | Pinned import elaborated and printed the exact types of kernel composition, its setwise integral rule, associativity, both Chapman-Kolmogorov candidates, and `IsMarkovKernel` |
| `rg -n 'pow_add_apply_eq_lintegral\|Chapman' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 0 | The only matches are the documented candidate family in `Mathlib/Probability/Kernel/Composition/Comp.lean` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git diff --check -- Stage1_Instances/THM-M-1091 .stage1-worker-selftest.json` | 0 | No whitespace errors |

## Result boundary

These checks self-test the assigned intake deliverable: membership, planned dossier structure,
source/scope crosswalk, JSON syntax, and actual availability of the pinned Lean candidates. They do
not select the homogeneous discrete-time specialization as the exact source theorem, establish a
primary-source premise crosswalk, freeze an expression hash, or credit the candidate proof bodies.
The exact-statement gate and all dependent nodes remain open. Theorem completion is false and no
accepted receipt is claimed.

The worktree contains the automation-provided untracked `Formalizations/Lean/.lake` link. It was
not created or modified for this item, and this worker evidence is nonrelease evidence.
