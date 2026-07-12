# THM-M-1045 obligation-tree validation

Item: `S56-M-1045-OBLIGATION_TREE`  
Base revision: `57fd3b3240d6c69ac3458640e129b3c0fea918fd`  
Validation date: 2026-07-12

The registry freezes 15 semantic obligations with denominator SHA-256
`4f4276a1fee35b49c4c791e689aa9ef32bd80319f08f8195a782aa82be8a08e3`.
The seven typed graphs contain 30 edges. Proof/composition edges expose three open branch packages;
source, documentation, provenance, trust, and workflow relations cannot supply proof credit.

## Commands and results

All commands ran in this worker clone. Lean reused the existing pinned Lake artifacts. No
`lake update`, build, fetch, clone, or dependency mutation ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-1045/build_obligation_artifacts.py` | 0 | deterministically emitted denominator `4f4276...08e3` |
| `python3 Stage1_Instances/THM-M-1045/check_obligation_tree.py` | 0 | 15 obligations, 30 typed edges, reciprocal proof edges, acyclic exact root reachability, node schemas, budgets, hashes, and open closure passed |
| pinned `lean` from `lake env which lean`, with `lake env printenv LEAN_PATH`, elaborating `Statement.lean` to a temporary local olean then `ObligationTree.lean` | 0 | exact conditional composition elaborated; axiom report was `[propext, Classical.choice, Quot.sound]`; temporary olean removed |
| `python3 -m json.tool` on the registry, graph bundle, and validation specs | 0 | all structured artifacts valid JSON |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets valid |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, uniform rework baseline |
| `python3 scripts/stage1_target.py show THM-M-1045` | 0 | rank 238, planned, theorem incomplete |
| forbidden-device scan of `ObligationTree.lean` | 1 | expected no-match exit; no `sorry`, `admit`, `axiom`, or `sorryAx` token |
| `git diff --check -- Stage1_Instances/THM-M-1045 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Status boundary

This phase is self-tested pending master acceptance. The root remains `M3`, with
`M1045-B-EQUIVALENCE`, `M1045-B-DENSITY`, and `M1045-B-SINGULARITY` as its open cut set. The
conditional certificate does not prove any branch. Human status remains `H1`, readability remains
`R3`, and neither audit nor theorem completion is claimed.
