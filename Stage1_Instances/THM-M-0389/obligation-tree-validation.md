# Obligation-tree validation record

Item: `S56-M-0389-OBLIGATION_TREE`  
Base revision: `4dabab14860067cbb1220d76c5a1bd9abd87d624`

## Frozen result

Registry version 1 freezes sixteen required obligations and zero exclusions.
The typed bundle separates proof, composition, refinement, provenance,
evidence, trust, documentation, and workflow edges. All fifteen mathematical
and statement nodes are reachable from the exact root in an acyclic proof
graph. The release trust node is connected only by `trusts`, because it is not
a mathematical premise.

The standalone Lean module checks the top-level zero/nonzero split and consumes
the zero-coordinate, sign-normalization, and positive-generation children to
produce the exact root shape. Its children remain hypotheses. The positive
descent child-to-parent composition and all unlocated bodies remain open.

## Validation

All commands ran in this worker clone using the existing pinned toolchain. No
dependency update, clone, fetch, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0389/ObligationTree.lean` | 0 | exact root fixture and conditional composition elaborate; `root_compose` reports no axioms |
| `python3 Stage1_Instances/THM-M-0389/check_obligation_tree.py` | 0 | 16 obligations, 14 proof edges, acyclic root reachability, all ledgers at most 100 |
| `python3 -m json.tool` on registry, graph bundle, and proof-unit manifest | 0 | all structured artifacts parse |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 structure and 1546 uniform-L0 target set pass |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets pass |
| `python3 scripts/stage1_target.py show THM-M-0389` | 0 | rank 20, planned, L0/rework-required, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0389 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Boundary

This is self-tested obligation-architecture evidence pending master acceptance.
It is not proof-phase closure or a hermetic/independent release replay. The root
remains `H4/M3/R3`; `audit_complete=false` and `theorem_complete=false`.
