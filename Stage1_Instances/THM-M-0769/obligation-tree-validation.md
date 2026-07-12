# THM-M-0769 obligation-tree validation

Item: `S56-M-0769-OBLIGATION_TREE`. Base revision:
`9864b47f2fbf53d0b642c54f12039877d4635056`.

Validation ran in the worker clone on 2026-07-12. It reused the existing pinned
Lake closure and did not update, build, fetch, or clone dependencies.

```text
python3 Stage1_Instances/THM-M-0769/build_obligation_artifacts.py
  exit 0
  denominator: 15be0f99726930b27ca32c833957ba0252d58df87699fedc79450003d6685e52

python3 Stage1_Instances/THM-M-0769/check_obligation_tree.py
  exit 0
  PASS THM-M-0769 obligation tree: 9 obligations, 24 typed edges
  root closure: open (M3); fiber choice and release overlays remain open

LEAN_BIN=$(cd Formalizations/Lean && lake env which lean)
LEAN_PATH=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
cd Stage1_Instances/THM-M-0769
LEAN_PATH="$LEAN_PATH" "$LEAN_BIN" -o Statement.olean Statement.lean
LEAN_PATH=".:$LEAN_PATH" "$LEAN_BIN" ObligationTree.lean
rm -f Statement.olean
  exit 0
  root_of_fiberSelector has the exact AxiomOfChoiceTarget conclusion
  root_of_fiberSelector does not depend on any axioms

python3 Docs/tools/check_stage1_standard.py
  exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets
python3 scripts/stage1_target.py check
  exit 0; 1546 unique targets, ranks 1..1546
python3 scripts/stage1_target.py show THM-M-0769
  exit 0; rank 779, planned, theorem_complete false
```

The first direct command, `cd Formalizations/Lean && lake env lean
../../Stage1_Instances/THM-M-0769/ObligationTree.lean`, exited 1 because the
target-local `Statement` module had no compiled object on that search path.
The corrected scoped recipe above derives the executable and dependency path
from Lake, writes `Statement.olean` only under the owned target, checks the
composition, and removes the temporary object.

The structural checker validates freeze hashes, immutable denominators,
eligibility projections, node schemas and budgets, all seven typed graph
adjacency maps, reciprocal proof edges, acyclic root reachability, recipe
coverage, the open-root boundary, and placeholder hygiene. Lean checks only
the conditional composition. The fiber selector remains an explicit premise,
so this phase proves no choice principle and claims no theorem completion.
