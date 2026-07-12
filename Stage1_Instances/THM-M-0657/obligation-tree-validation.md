# THM-M-0657 obligation-tree validation

Item: `S56-M-0657-OBLIGATION_TREE`. Base revision:
`6446a4b59b8c8950aa4ba92ab10c8d025ce57fc7`.

Validation ran in the worker clone on 2026-07-12. Existing canonical pinned
Lake artifacts were reused. No update, build, dependency fetch, or clone was
run.

```text
python3 Stage1_Instances/THM-M-0657/build_obligation_artifacts.py
  exit 0
  22647d29b16c9d77f04719fe51238e427dab88b5fd6c57dfab8ac599c627ce44

python3 Stage1_Instances/THM-M-0657/check_obligation_tree.py
  exit 0
  PASS THM-M-0657 obligation tree: 14 obligations, 56 typed edges
  registry denominator sha256: 22647d29b16c9d77f04719fe51238e427dab88b5fd6c57dfab8ac599c627ce44
  root closure: open (M3); substantive completeness, stability, saturation,
  existence, uniqueness, source, and trust obligations remain open

LEAN_BIN=$(cd Formalizations/Lean && lake env which lean)
LEAN_PATH=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
cd Stage1_Instances/THM-M-0657
LEAN_PATH="$LEAN_PATH" "$LEAN_BIN" -o Statement.olean Statement.lean
LEAN_PATH=".:$LEAN_PATH" "$LEAN_BIN" ObligationTree.lean
rm -f Statement.olean
  exit 0
  root_of_transferPackage depends on axioms:
  [propext, Classical.choice, Quot.sound]

python3 Docs/tools/check_stage1_standard.py
  exit 0; 15 assurance groups and 1546 uniform-L0 targets

python3 scripts/stage1_target.py check
  exit 0; 1546 unique targets, ranks 1..1546

python3 scripts/stage1_target.py show THM-M-0657
  exit 0; rank 702, planned, theorem_complete false
```

The structural checker binds the freeze to the statement and anchor-audit
hashes, recomputes the denominator, checks eligibility projections, requires
the full node schema and step budgets, verifies typed adjacency and reciprocal
proof edges, rejects proof cycles, checks validation-recipe coverage, and scans
the Lean harness for forbidden proof escapes. Lean elaborates the exact
statement and conditional terminal boundary using the pinned toolchain.

This evidence validates registry and graph structure only. The conditional
terminal declaration consumes the exact result as an input, so its axiom report
does not constitute a Morley proof or any child closure. Primary-source mapping,
formal proof bodies, transitive trust audit, audit completion, theorem
completion, and master acceptance remain open.
