# THM-M-0773 obligation-tree validation

Item: `S56-M-0773-OBLIGATION_TREE`. Base revision:
`444819795285695894ff7b29af5c2419e0e000fa`.

Validation ran in the worker clone on 2026-07-12. It reused the existing pinned
Lake closure and did not update, build, fetch, clone, or modify dependencies.

```text
python3 Stage1_Instances/THM-M-0773/build_obligation_artifacts.py
  exit 0
  denominator: 8f19a683c860e2b4563adc27ea17d4d49dd0d899f93a165e6cc5568a0abe4bee

python3 Stage1_Instances/THM-M-0773/check_obligation_tree.py
  exit 0
  PASS THM-M-0773 obligation tree: 10 obligations, 22 typed edges
  root closure: open (M3); pointed bridge and assurance overlays remain unaccepted

LEAN_BIN=$(cd Formalizations/Lean && lake env which lean)
LEAN_PATH=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
cd Stage1_Instances/THM-M-0773
LEAN_PATH="$LEAN_PATH" "$LEAN_BIN" -o Statement.olean Statement.lean
LEAN_PATH=".:$LEAN_PATH" "$LEAN_BIN" ObligationTree.lean
rm -f Statement.olean
  exit 0
  root_of_pointedPackage has the exact TeichmullerTukeyTarget conclusion
  root_of_pointedPackage does not depend on any axioms

python3 Docs/tools/check_stage1_standard.py
  exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets
python3 scripts/stage1_target.py check
  exit 0; 1546 unique targets, ranks 1..1546
python3 scripts/stage1_target.py show THM-M-0773
  exit 0; rank 781, planned, theorem_complete false
git diff --check -- Stage1_Instances/THM-M-0773
  exit 0; no output
```

The structural checker validates frozen input hashes, the immutable denominator
and eligibility projections, unique node and edge IDs, all seven typed graph
adjacency maps, reciprocal proof edges, acyclic root reachability, per-node
validation recipes, step budgets, placeholder hygiene, and the open-root
boundary. Lean validates only the conditional composition. The pointed package
is an explicit premise, so this phase supplies no accepted proof-body credit and
makes no theorem-completion claim.
