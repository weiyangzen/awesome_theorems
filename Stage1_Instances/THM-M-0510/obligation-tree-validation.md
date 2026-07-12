# THM-M-0510 obligation-tree validation

Item: `S56-M-0510-OBLIGATION_TREE`. Base revision:
`e9252b1cfdc99a094324c8a10d260769df2eca15`.

Validation ran in this worker clone on 2026-07-12. Existing pinned Lake
artifacts were reused; no update, build, dependency fetch, or clone was run.

```text
python3 Stage1_Instances/THM-M-0510/build_obligation_artifacts.py
  exit 0
  59e9147cc46427b6fc6a114cf81f7a5710c3441cf3a9ef2a74b1690f08f167dd

python3 Stage1_Instances/THM-M-0510/check_obligation_tree.py
  exit 0
  PASS THM-M-0510 obligation tree: 17 obligations, 59 typed edges
  registry denominator sha256: 59e9147cc46427b6fc6a114cf81f7a5710c3441cf3a9ef2a74b1690f08f167dd
  root closure: open (M3); all analytic circle-method bodies remain open

cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0510/Statement.lean
  exit 0; exact canonical statement re-elaborated

LEAN_BIN=$(cd Formalizations/Lean && lake env which lean)
LEAN_PATH=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
cd Stage1_Instances/THM-M-0510
LEAN_PATH="$LEAN_PATH" "$LEAN_BIN" -o Statement.olean Statement.lean
LEAN_PATH=".:$LEAN_PATH" "$LEAN_BIN" ObligationTree.lean
rm -f Statement.olean
  exit 0
  root_of_finalAsymptotic depends on axioms: [propext, Classical.choice, Quot.sound]

python3 Docs/tools/check_stage1_standard.py
  exit 0; 15 assurance groups and 1546 uniform-L0 targets passed
python3 scripts/stage1_target.py check
  exit 0; 1546 unique targets, ranks 1 through 1546
python3 scripts/stage1_target.py show THM-M-0510
  exit 0; rank 884, planned, theorem_complete false
git diff --check -- Stage1_Instances/THM-M-0510
  exit 0; no whitespace errors
```

The first direct `lake env lean ../../Stage1_Instances/THM-M-0510/ObligationTree.lean`
attempt exited 1 because `import Statement` requires a local olean in Lean's search
path. The corrected narrow recipe above uses the Lake-selected Lean executable and
`LEAN_PATH`, creates `Statement.olean` only inside the owned directory, validates the
dependent module, and removes the temporary artifact.

The structural checker binds the registry to the statement and anchor-audit bytes,
checks the immutable denominator and all eligibility projections, verifies the full
required node schema, reciprocal proof edges, adjacency, acyclicity, recipe coverage,
closure boundary, and placeholder hygiene. Lean checks the exact output transport and
reports its axiom closure. This does not validate any circle-method proof body,
child-to-parent analytic composition, H0 source closure, R0 reconstruction, transitive
trust closure, or theorem completion. Master acceptance remains required.
