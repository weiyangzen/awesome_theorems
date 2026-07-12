# THM-M-0644 obligation-tree validation

Item: `S56-M-0644-OBLIGATION_TREE`. Base revision:
`2414fa7f8693bbe8d5b656241466f11ec0430a5f`.

Validation ran in the worker clone on 2026-07-12 using the existing pinned Lake artifacts. No
dependency update, build, fetch, or clone was run.

```text
python3 Stage1_Instances/THM-M-0644/build_obligation_artifacts.py
  exit 0
  wrote 16 obligations and 45 typed edges
  denominator: 9ab14663c4b58cc39a43be9f8c1a4d58317d42f937f75b308629cda702756dac

python3 Stage1_Instances/THM-M-0644/check_obligation_tree.py
  exit 0
  PASS THM-M-0644 obligation tree: 16 obligations, 45 typed edges
  root closure: open (M3); accepted direction and provenance receipts remain deferred

cd Formalizations/Lean &&
  lake env lean ../../Stage1_Instances/THM-M-0644/ObligationTree.lean
  exit 0
  root_of_directions elaborated at the exact target type
  axiom output: [propext, Quot.sound]

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets valid
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1 through 1546
python3 scripts/stage1_target.py show THM-M-0644
  exit 0: rank 690, planned, theorem_complete false
git diff --check -- Stage1_Instances/THM-M-0644
  exit 0; no output
```

The structural validator checks source freeze hashes, the canonical denominator hash, required
node fields, step budgets, typed endpoint legality, reciprocal proof/composition edges, adjacency,
acyclic root reachability, recipe coverage, hygiene, and the explicit open-root boundary. Lean
checks the conditional two-direction composition without `sorry`, `axiom`, or placeholders.

This evidence freezes the obligation architecture only. The root remains `M3`; accepted proof,
primary-source mapping, transitive provenance/trust, audit completion, release validation, and
theorem completion remain open. There is no master acceptance receipt.
