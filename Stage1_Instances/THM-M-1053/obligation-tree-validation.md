# THM-M-1053 obligation-tree validation

Item: `S56-M-1053-OBLIGATION_TREE`  
Base revision: `3ec252ff03162db067bf77973c0a74a97d4bbe0a`  
Validation date: 2026-07-12

The worker reused the existing pinned Lake artifacts. No update, build, clone,
fetch, or dependency mutation ran.

## Commands and results

```text
python3 Stage1_Instances/THM-M-1053/build_obligation_artifacts.py
  exit 0
  125e28fed0cbce9e0cbffea0da90b047c35a770c90d3be2a82a42319b8606005

python3 Stage1_Instances/THM-M-1053/check_obligation_tree.py
  exit 0
  PASS THM-M-1053 obligation tree: 16 obligations, 35 typed edges
  registry denominator sha256: 125e28fed0cbce9e0cbffea0da90b047c35a770c90d3be2a82a42319b8606005
  root closure: open (M1); general-limit and ergodic-identification packages remain open

cd Stage1_Instances/THM-M-1053 &&
  LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    $(cd ../../Formalizations/Lean && lake env which lean) -o Statement.olean Statement.lean &&
  LEAN_PATH=.:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    $(cd ../../Formalizations/Lean && lake env which lean) ObligationTree.lean
  exit 0
  Statement and exact conditional child-to-root composition elaborated;
  `#print axioms` reported `[propext, Classical.choice, Quot.sound]`.
  The temporary `Statement.olean` was removed.

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets valid
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, uniform L0/rework-required
python3 scripts/stage1_target.py show THM-M-1053
  exit 0: rank 245, planned, theorem_complete false
python3 -m json.tool on instance.json, obligation-registry.json,
  typed-graphs.json, and validation-specs.json
  exit 0 for all four
git diff --check -- Stage1_Instances/THM-M-1053 .stage1-worker-selftest.json
  exit 0; no output
```

The structural check validates frozen input hashes and canonical denominator,
all required node fields and budgets, typed endpoints and adjacency, reciprocal
proof/composition edges, acyclicity, exact root reachability, validation-recipe
coverage, fail-closed closure status, and placeholder hygiene. The Lean check
validates only the conditional composition and proves neither input package.

## Status boundary

This phase is self-tested pending master acceptance. The minimal open root cut
is `M1053-T-GENERAL` plus `M1053-L-ERGODIC-IDENTIFICATION`. The external exact
candidate remains outside the pinned dependency closure. Root status stays
`H2/M1/R4`; there is no root closure, accepted receipt, audit completion, or
theorem completion.
