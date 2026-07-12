# THM-M-0452 obligation-tree validation

Item: `S56-M-0452-OBLIGATION_TREE`. Base revision:
`12c908b3643c2473ee5e87f188ece1d3d8081640`.

Validation ran in the worker clone on 2026-07-12. It reused the existing pinned
Lake dependency closure and did not update, fetch, clone, or build dependencies.

```text
python3 Stage1_Instances/THM-M-0452/build_obligation_artifacts.py
  exit 0
  wrote 23 obligations and 51 typed edges
  44e12aea29ad4e5c8ba45851e7809810040ba4f5ae85a442c7a65ebe11fad115

python3 Stage1_Instances/THM-M-0452/check_obligation_tree.py
  exit 0
  PASS THM-M-0452 obligation tree: 23 obligations, 51 typed edges
  registry denominator sha256: 44e12aea29ad4e5c8ba45851e7809810040ba4f5ae85a442c7a65ebe11fad115
  root closure: open (M3); height, polarization, and quotient packages remain M4

LEAN_BIN=$(cd Formalizations/Lean && lake env which lean)
LEAN_DEPS=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
cd Stage1_Instances/THM-M-0452
LEAN_PATH="$LEAN_DEPS" "$LEAN_BIN" -o Statement.olean Statement.lean
LEAN_PATH=".:$LEAN_DEPS" "$LEAN_BIN" ObligationTree.lean
rm -f Statement.olean
  exit 0
  exact canonical target printed
  root_of_height_polarization_quotient depends on axioms:
    [propext, Classical.choice, Quot.sound]

python3 Docs/tools/check_stage1_standard.py
  exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets
python3 scripts/stage1_target.py check
  exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-0452
  exit 0; rank 301, planned, legacy artifacts unaccepted, theorem_complete false
python3 -m json.tool obligation-registry.json typed-graphs.json validation-specs.json
  exit 0 for each JSON file
rg line-leading prohibited declarations and sorryAx in Statement.lean and ObligationTree.lean
  exit 1 as expected (no matches); treated as hygiene success
git diff --check -- Stage1_Instances/THM-M-0452 .stage1-worker-selftest.json
  exit 0; no output
```

The checks validate source-bound registry hashes, frozen denominators, node
ledgers and budgets, typed reciprocal proof edges, graph adjacency, proof-DAG
reachability, validation coverage, prohibited-token hygiene, and a kernel-
elaborated conditional composition into the exact root. The temporary sibling
`Statement.olean` was removed after the narrow check.

This phase does not construct a canonical height, prove its quadraticity or
torsion kernel, descend the pairing, establish H0/R0, complete the audit, or
satisfy any release gate. There is no accepted receipt and master acceptance
is still required.
