# THM-M-0653 obligation-tree validation

Item: `S56-M-0653-OBLIGATION_TREE`. Base revision:
`16187d91397de4edab8cb93140166f634baa0c02`.

Validation ran in the worker clone on 2026-07-12. Existing pinned Lake
artifacts were reused; no update, build, fetch, or clone was run.

```text
python3 Stage1_Instances/THM-M-0653/build_obligation_artifacts.py
  exit 0
  9fcae8472275eba1ab3f0c54ffd92fa5f68b0c04d2bf7c5d8723036e94072eb6

python3 Stage1_Instances/THM-M-0653/check_obligation_tree.py
  exit 0
  PASS THM-M-0653 obligation tree: 14 obligations, 49 typed edges
  registry denominator sha256: 9fcae8472275eba1ab3f0c54ffd92fa5f68b0c04d2bf7c5d8723036e94072eb6
  root closure: open (M3); Beth and converse direction packages remain open

LEAN_BIN=$(cd Formalizations/Lean && lake env which lean)
LEAN_PATH=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
cd Stage1_Instances/THM-M-0653
LEAN_PATH="$LEAN_PATH" "$LEAN_BIN" -o Statement.olean Statement.lean
LEAN_PATH=".:$LEAN_PATH" "$LEAN_BIN" ObligationTree.lean
rm -f Statement.olean
  exit 0
  BethDefinabilityTarget.{u, v, w} ... : Prop
  root_of_directions depends on axioms: [Quot.sound]

python3 Docs/tools/check_stage1_standard.py
  exit 0; 15 assurance groups and 1546 uniform-L0 targets
python3 scripts/stage1_target.py check
  exit 0; 1546 unique targets, ranks 1..1546
python3 scripts/stage1_target.py show THM-M-0653
  exit 0; rank 698, planned, theorem_complete false
```

An initial scoped Lean command from `Formalizations/Lean` failed because Lean
4.29 requires the input to be beneath the package root and therefore did not
produce `Statement.olean`; this failed attempt is retained here as evidence of
the corrected validation boundary. The successful command uses the exact
`lake env which lean` executable and Lake-derived pinned `LEAN_PATH`, writes a
temporary olean only inside the owned target, and removes it.

The structural checker validates source freeze hashes, the immutable registry
denominator, eligibility projections, typed graph adjacency, reciprocal proof
edges, acyclicity, validation-recipe coverage, and placeholder hygiene. Lean
validates the exact statement and root-type identity boundary. It does not
validate a Beth proof, directional composition, source closure, or theorem
completion. Master acceptance remains required.
