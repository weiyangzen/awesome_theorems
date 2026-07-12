# THM-M-0118 obligation-tree validation

Item: `S56-M-0118-OBLIGATION_TREE`. Base revision:
`2029732601188918961647a1d1565c7d55a46f04`.

Validation ran in this worker clone on 2026-07-12 using the existing pinned
Lake dependency closure. No update, fetch, clone, dependency build, or `.lake`
mutation was performed.

```text
python3 Stage1_Instances/THM-M-0118/build_obligation_artifacts.py
  exit 0
  8425e616e49a6e99bb1bf6c26f80f255b59b15471694cafeac45df69b616ce22

python3 Stage1_Instances/THM-M-0118/check_obligation_tree.py
  exit 0
  PASS THM-M-0118 obligation tree: 14 obligations, 62 typed edges
  root closure: open (M3); native analytic and cohomology transport package remains M4

LEAN_BIN=$(cd Formalizations/Lean && lake env which lean)
LEAN_DEPS=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
cd Stage1_Instances/THM-M-0118
LEAN_PATH="$LEAN_DEPS" "$LEAN_BIN" -o Statement.olean Statement.lean
LEAN_PATH=".:$LEAN_DEPS" "$LEAN_BIN" ObligationTree.lean
rm -f Statement.olean
  exit 0
  nakanoVanishingTarget_of_analyticPackage does not depend on any axioms
  analyticPackage_iff_target does not depend on any axioms

python3 Docs/tools/check_stage1_standard.py
  exit 0; 15 assurance groups and 1546 uniform-L0 targets
python3 scripts/stage1_target.py check
  exit 0; 1546 unique targets, ranks 1..1546
python3 scripts/stage1_target.py show THM-M-0118
  exit 0; rank 329, planned, theorem_complete false
python3 -m json.tool on obligation-registry.json, typed-graphs.json,
validation-specs.json
  exit 0 for all three files
scoped prohibited-token scan of Statement.lean and ObligationTree.lean
  exit 0; no sorry, admit, axiom declaration, or sorryAx
git diff --check -- Stage1_Instances/THM-M-0118
  exit 0; no output
```

One initial direct elaboration from `Formalizations/Lean` exited 1 because the
sibling `Statement` module had no `.olean` on the import path. The successful
scoped recipe above derives the exact executable and dependency path from the
pinned Lake environment, emits `Statement.olean` beside its source, elaborates
the dependent module, and removes the temporary artifact. This setup failure
is recorded rather than hidden and was not a source elaboration failure.

These checks validate source-bound hashes, frozen denominators and eligibility,
node ledgers and budgets, seven disjoint typed graph families, reciprocal proof
edges, DAG reachability, structured recipe coverage, hygiene, and the exact
conditional composition. They do not prove the analytic premise, close the
root, establish H0/R0, or satisfy a theorem-release gate. Master acceptance is
still required.
