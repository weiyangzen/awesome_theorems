# THM-M-1291 obligation-tree validation

Item: `S56-M-1291-OBLIGATION_TREE`. Base revision:
`b057c8113d3f265874a1fdf670b1ab3558dc8a28`.

Validation ran in the worker clone on 2026-07-12. It reused the existing pinned
Lake closure and did not update, fetch, clone, or build dependencies.

```text
python3 Stage1_Instances/THM-M-1291/build_obligation_artifacts.py
  exit 0; generated 17 obligations and 38 typed edges
  denominator: 4331556ba27d32b56189b66a2438dd243ec27af5396f615cc98bb7a763be4748

python3 Stage1_Instances/THM-M-1291/check_obligation_tree.py
  exit 0; PASS THM-M-1291 obligation tree: 17 obligations, 38 typed edges
  root closure: open (M3); corrected-remainder integral convergence remains M4

cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1291/Statement.lean
  exit 0; printed the fully explicit canonical BrezisLiebTarget

python3 Docs/tools/check_stage1_standard.py
  exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets
python3 scripts/stage1_target.py check
  exit 0; 1546 unique targets, ranks 1..1546
python3 scripts/stage1_target.py show THM-M-1291
  exit 0; rank 462, planned, theorem_complete false
```

The structural check verifies source hashes, frozen denominators, eligibility,
node ledgers and budgets, edge adjacency, reciprocal proof edges, acyclic root
reachability, recipe coverage, the open-root boundary, and token hygiene. It
does not prove a mathematical obligation or satisfy a theorem-release gate.
