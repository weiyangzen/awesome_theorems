# THM-M-0696 obligation-tree validation

Item: `S56-M-0696-OBLIGATION_TREE`. Base revision:
`f4c286c4ebc4a8b1a5d0a746afd6fba9849e4c7c`.

Validation ran in the worker clone on 2026-07-12. Existing pinned Lake artifacts were reused; no
update, build, fetch, or clone was run.

```text
python3 Stage1_Instances/THM-M-0696/build_obligation_artifacts.py
  exit 0
  08af7ce3485e5731b36f690772b702762d8c13c1e30732977b25a8a02a30554b

python3 Stage1_Instances/THM-M-0696/check_obligation_tree.py
  exit 0
  PASS THM-M-0696 obligation tree: 17 obligations, 60 typed edges
  registry denominator sha256: 08af7ce3485e5731b36f690772b702762d8c13c1e30732977b25a8a02a30554b
  root closure: open (M3); countermodel package is the first open cut set

LEAN_BIN=$(cd Formalizations/Lean && lake env which lean)
LEAN_PATH=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
cd Stage1_Instances/THM-M-0696
LEAN_PATH="$LEAN_PATH" "$LEAN_BIN" -o Statement.olean Statement.lean
LEAN_PATH=".:$LEAN_PATH" "$LEAN_BIN" ObligationTree.lean
rm -f Statement.olean
  exit 0
  all five planned interfaces elaborate
  completeness_of_countermodel depends on axioms: [propext, Classical.choice, Quot.sound]
```

The first Lean attempt exposed a missing local `Decidable (Derives ...)` instance in the canonical
valuation definition and exited 1. The definition was corrected to make its classical decision
boundary explicit; the successful rerun above is the self-test result. The generated temporary
`Statement.olean` stayed inside the owned target and was removed.

The structural checker binds the registry to the exact statement and anchor-audit byte hashes,
recomputes the frozen denominator, checks required node fields and leaf budgets, verifies typed
adjacency and reciprocal proof/composition edges, rejects proof cycles, covers every node with a
validation recipe, scans the Lean architecture file for forbidden placeholders, and asserts the
fail-closed root state. Lean checks the planned interfaces and exact child-to-root composition. It
does not prove the countermodel package or any of its open children, accept source/readability
reviews, establish release trust, or complete the theorem. Master acceptance remains required.
