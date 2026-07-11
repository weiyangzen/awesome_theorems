# THM-M-0088 obligation-tree validation

Item: `S56-M-0088-OBLIGATION_TREE`. Base revision:
`cd2070316d8a25117b90105fb1da2b6853a71999`.

Validation ran inside the worker clone on 2026-07-12. It reused the existing pinned Lake artifacts;
no dependency update, fetch, clone, or build was run. The authoritative blueprint and DAG were
already modified outside this item and were not touched by this worker.

```text
python3 Stage1_Instances/THM-M-0088/build_obligation_artifacts.py
  exit 0
  01bf9d82833b993ab47ace9bd1ef7e062bb4f37fa6801d241f51a1cef457b150

python3 Stage1_Instances/THM-M-0088/check_obligation_tree.py
  exit 0
  PASS THM-M-0088 obligation tree: 8 obligations, 21 typed edges
  registry denominator sha256: 01bf9d82833b993ab47ace9bd1ef7e062bb4f37fa6801d241f51a1cef457b150
  root closure: open (M3); preimage and inverse-law leaves remain M4

cd Stage1_Instances/THM-M-0088 &&
  LEAN_BIN=$(cd ../../Formalizations/Lean && lake env which lean) &&
  LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) &&
  LEAN_PATH="$LEAN_PATH" "$LEAN_BIN" -o Statement.olean Statement.lean &&
  LEAN_PATH=.:"$LEAN_PATH" "$LEAN_BIN" ObligationTree.lean
  exit 0
  yonedaEmbedding_of_inverseLaws elaborated with the exact YonedaEmbeddingTarget result
  declaration axioms: [propext, Classical.choice, Quot.sound]
  The temporary Statement.olean was removed after the scoped check.

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets consistent
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-0088
  exit 0: rank 137, planned, theorem_complete false
git diff --check -- Stage1_Instances/THM-M-0088
  exit 0: no whitespace errors
```

The structural check binds the registry to the exact statement and anchor-audit bytes, recomputes
the denominator, checks eligibility projections, node ledgers and budgets, all seven graph classes,
reciprocal proof/composition edges, acyclicity, root reachability, structured recipe coverage, and
the open closure boundary. The Lean check validates only the conditional constructor composition.
It does not credit the audited imported anchor or prove the preimage and inverse-law leaves.

Root debt remains `[H1, M3, R3]`. Audit completion, theorem completion, accepted receipts, and
master acceptance are explicitly outside this worker phase.
