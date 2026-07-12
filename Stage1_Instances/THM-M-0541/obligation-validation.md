# THM-M-0541 obligation-tree validation

Item: `S56-M-0541-OBLIGATION_TREE`  
Base revision: `8ac609b6e17629674e5bb3f43384178e23cf0da8`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

The frozen registry contains 36 unique obligations: 35 required mathematical nodes and one
informational trust overlay. The validator recomputed the denominator digest, checked all required
node fields, enforced `<=100` budgets only on leaf-shaped nodes, checked reciprocal indexes and
unique IDs across seven typed graphs, proved the combined proof/refinement graph acyclic, and
verified root reachability for every required machine obligation. There are 54 typed edges.

The exact `StatementShape` separately re-elaborated using the existing pinned `.lake` artifacts,
and all four statement mutations remained distinct. No `lake update`, `lake build`, dependency
clone/fetch, or `.lake` mutation was performed.

## Commands and exact outcomes

| command | exit | outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets and ranks 1..1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0541` | 0 | rank 598, planned, L0/rework-required, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0541/Statement.lean)` | 0 | exact `StatementShape` elaborated |
| `python3 Stage1_Instances/THM-M-0541/check_statement.py` | 0 | statement digest `95f44477...0577b44e1`; four mutations killed; pinned revisions matched |
| `python3 Stage1_Instances/THM-M-0541/check_obligation_tree.py` | 0 | `PASS`: 36 obligations, 54 typed edges; root open M3 |
| `python3 -m json.tool Stage1_Instances/THM-M-0541/obligation-registry.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0541/typed-graphs.json` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0541 .stage1-worker-selftest.json` | 0 | no whitespace errors |

Content hashes after validation:

```text
fa62c038bcf08222c22cb315901d214106c5ed23dbde31868687b1ee29f2ae04  obligation-registry.json
2aa9d617b073acfc8b1ff5e72fc42993b95d5a209ee5b85eedf0e824fa3c8d9e  typed-graphs.json
```

## Status boundary

This evidence self-tests only the registry and graph freeze. Planned fingerprints and budgets are
not Lean proofs. No node has a proof body, source review, composition certificate, trust closure,
or readable review. The first root cut remains `M0541-C3`, `M0541-L1`, `M0541-L4`, and
`M0541-T2`; no audit or theorem completion is claimed. Master acceptance is still required.

