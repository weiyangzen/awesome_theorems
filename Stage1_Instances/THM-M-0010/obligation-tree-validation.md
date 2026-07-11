# Obligation-tree validation record

Item: `S56-M-0010-OBLIGATION_TREE`  
Base revision: `2b4eb35cef43c30717c7567d9fa2e213428a17c6`

All commands ran in this worker automation clone on 2026-07-12. The Lean check
used the existing pinned `.lake` link. No dependency update, fetch, build, or
cache mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-0010/build_obligation_artifacts.py` | 0 | deterministically wrote registry, seven typed graph families, and validation specs; denominator `cad255...9cc` |
| `python3 Stage1_Instances/THM-M-0010/check_obligation_tree.py` | 0 | `PASS`; 10 unique obligations, hash binding, node fields, budgets, graph endpoints, reciprocal proof edges, acyclicity, recipes, and open-root boundary checked |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0010/ObligationTree.lean` | 0 | all three stable-filtration declarations and exact upstream theorem resolved; conditional composition elaborated; axioms `[propext, Classical.choice, Quot.sound]` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard and 1546-target coverage passed |
| `python3 scripts/stage1_target.py check` | 0 | ordered manifest of 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py show THM-M-0010` | 0 | execution rank 103, planned, L0/rework-required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0010/obligation-registry.json` | 0 | registry JSON parsed |
| `python3 -m json.tool Stage1_Instances/THM-M-0010/typed-graphs.json` | 0 | typed graph JSON parsed |
| `python3 -m json.tool Stage1_Instances/THM-M-0010/validation-specs.json` | 0 | validation recipe JSON parsed |
| `git diff --check -- Stage1_Instances/THM-M-0010 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The first attempted combined command was launched from `Formalizations/Lean`
with a root-relative Python path and exited 2 because that path did not exist
from the selected working directory. It changed nothing. The corrected Python
commands above ran at repository root, and the required Lean command ran from
`Formalizations/Lean`.

## Status boundary

The obligation registry and typed proof, refinement, provenance, evidence,
trust, documentation, and workflow graphs are self-tested pending master
acceptance. This architecture check makes no proof-node or theorem-completion
claim.
