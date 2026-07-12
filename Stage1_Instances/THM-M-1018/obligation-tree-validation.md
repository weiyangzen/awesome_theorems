# Obligation-tree validation receipt

Item: `S56-M-1018-OBLIGATION_TREE`  
Date: 2026-07-12  
Base revision: `205d13cfc35c45883410c569709a91cb34edce16`

## Scope

This receipt validates registry/graph structure, frozen input hashes, reciprocal proof edges,
acyclic root reachability, executable validation specifications, the absence of forbidden Lean
placeholders, and the conditional child-to-root composition. It is nonrelease worker evidence.
The root remains `M3`; `M1018-T-ANALYTIC` is the open cut.

## Exact commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-1018/build_obligation_artifacts.py` | 0 | regenerated the frozen registry, seven typed graphs, and validation specifications; denominator digest recorded in JSON |
| `python3 Stage1_Instances/THM-M-1018/check_obligation_tree.py` | 0 | 17 obligations and all typed edges passed structural, hash, reciprocity, reachability, budget, recipe, and status-boundary checks |
| `lake env lean ../../Stage1_Instances/THM-M-1018/ObligationTree.lean` from `Formalizations/Lean` | 0 | the duplicated exact kernel interface, `InversionFor`, and conditional binder-expanded `root_compose` elaborated; axiom report was `[propext, Classical.choice, Quot.sound]` |
| `lake env lean ../../Stage1_Instances/THM-M-1018/Statement.lean` from `Formalizations/Lean` | 0 | frozen exact statement, checked transport, mutations, and printed root elaborated |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets passed |
| `python3 scripts/stage1_target.py show THM-M-1018` | 0 | rank 494; lifecycle planned; theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1018/obligation-registry.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1018/typed-graphs.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1018/validation-specs.json` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1018 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Boundary

The conditional composition consumes rather than proves the analytic premise. No primary-source,
proof, provenance closure, audit completion, theorem completion, release, or master-acceptance
credit follows from this receipt.
