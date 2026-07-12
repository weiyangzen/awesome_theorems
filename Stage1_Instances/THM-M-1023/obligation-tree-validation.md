# THM-M-1023 obligation-tree validation

Item: `S56-M-1023-OBLIGATION_TREE`  
Base revision: `10f401f7930445a054adc972ae261c1a33df716e`  
Validation date: 2026-07-12

The worker reused the existing pinned Lake artifacts. No update, build, clone,
fetch, or dependency mutation was run.

## Commands and results

```text
python3 Stage1_Instances/THM-M-1023/build_obligation_artifacts.py
  exit 0
  d4c7d2a1d47477fc812ed85f49f768034a99424755d90cb4de202a112a80c825

python3 Stage1_Instances/THM-M-1023/check_obligation_tree.py
  exit 0
  PASS THM-M-1023 obligation tree: 17 obligations, 46 typed edges
  registry denominator sha256: d4c7d2a1d47477fc812ed85f49f768034a99424755d90cb4de202a112a80c825
  root closure: open (M3); forward and reverse packages remain M4

cd Formalizations/Lean &&
  lake env lean ../../Stage1_Instances/THM-M-1023/Statement.lean &&
  lake env lean ../../Stage1_Instances/THM-M-1023/ObligationTree.lean
  exit 1 after Statement.lean elaborated: the second input imports `Statement`,
  but no Statement.olean existed on LEAN_PATH. This failed invocation made no
  proof claim and was replaced by the package-root-independent recipe below.

LEAN_PATH=$(cd Formalizations/Lean && lake env printenv LEAN_PATH) \
  $(cd Formalizations/Lean && lake env which lean) \
    -o Stage1_Instances/THM-M-1023/Statement.olean \
    Stage1_Instances/THM-M-1023/Statement.lean &&
LEAN_PATH=Stage1_Instances/THM-M-1023:$(cd Formalizations/Lean && lake env printenv LEAN_PATH) \
  $(cd Formalizations/Lean && lake env which lean) \
    Stage1_Instances/THM-M-1023/ObligationTree.lean
  exit 0
  The exact statement and conditional composition elaborated. `#print axioms`
  reported `[propext, Classical.choice, Quot.sound]`. The temporary olean was
  removed after the check.

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets valid
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, uniform L0/rework-required
python3 scripts/stage1_target.py show THM-M-1023
  exit 0: rank 499, planned, theorem_complete false
python3 -m json.tool on obligation-registry.json, typed-graphs.json,
  validation-specs.json, and instance.json
  exit 0 for all four
git diff --check -- Stage1_Instances/THM-M-1023
  exit 0; no output
```

The structural validator checks frozen input hashes, the canonical denominator,
required node fields, budgets at most 100, edge endpoints and adjacency,
reciprocal proof/composition edges, proof-DAG acyclicity and reachability,
recipe coverage, closure boundaries, and Lean placeholder hygiene. The Lean
check proves only that exact forward and reverse packages compose to the exact
root. It does not inhabit either package.

## Status boundary

This phase is self-tested pending master acceptance. The registry and graphs
are frozen, but the root remains `[H1, M3, R4]`; the minimal open cut is
`M1023-T-FORWARD` plus `M1023-T-REVERSE`. There is no accepted receipt, source
completion, audit completion, or theorem completion.
