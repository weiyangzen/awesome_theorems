# THM-M-0612 obligation-tree validation

Item: `S56-M-0612-OBLIGATION_TREE`. Base revision:
`578632bf0c98d5485dbd13f1946157f593e5087a`.

Validation ran in the worker clone on 2026-07-12. It reused the existing pinned
Lake dependency closure and did not update, fetch, clone, or build dependencies.

```text
python3 Stage1_Instances/THM-M-0612/build_obligation_artifacts.py
  exit 0
  wrote 26 obligations and 58 typed edges
  2cad29b7c0b54afdec80a5d7ac1940a49cccfacdab64c1b75c27e140dd7a4bc8

python3 Stage1_Instances/THM-M-0612/check_obligation_tree.py
  exit 0
  PASS THM-M-0612 obligation tree: 26 obligations, 58 typed edges
  registry denominator sha256: 2cad29b7c0b54afdec80a5d7ac1940a49cccfacdab64c1b75c27e140dd7a4bc8
  root closure: open (M3); the radius-squared geometric package remains M4

LEAN_BIN=$(cd Formalizations/Lean && lake env which lean)
LEAN_DEPS=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
cd Stage1_Instances/THM-M-0612
LEAN_PATH="$LEAN_DEPS" "$LEAN_BIN" -o Statement.olean Statement.lean
LEAN_PATH=".:$LEAN_DEPS" "$LEAN_BIN" ObligationTree.lean
rm -f Statement.olean
  exit 0
  radius_le_of_sq_le depends on [propext, Classical.choice, Quot.sound]
  root_of_radiusSquaredObstruction depends on [propext, Classical.choice, Quot.sound]

python3 Docs/tools/check_stage1_standard.py
  exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets
python3 scripts/stage1_target.py check
  exit 0; 1546 unique targets, ranks 1..1546
python3 scripts/stage1_target.py show THM-M-0612
  exit 0; rank 256, planned, theorem_complete false
python3 -m json.tool on obligation-registry.json, typed-graphs.json,
validation-specs.json
  exit 0 for all three files
scoped prohibited-token scan of Statement.lean and ObligationTree.lean
  exit 0; no sorry, admit, axiom declaration, or sorryAx
git diff --check -- Stage1_Instances/THM-M-0612
  exit 0; no output
```

An initial direct elaboration of `ObligationTree.lean` from
`Formalizations/Lean` exited 1 because the sibling `Statement` module had no
`.olean` in the import path. A second attempt to emit that `.olean` from
outside Lake's root also exited 1 with Lean's root-containment check. The
successful scoped recipe above uses the exact pinned executable and
Lake-derived dependency path, emits `Statement.olean` beside the source, and
removes it after checking. These failed setup attempts are recorded rather
than hidden; neither indicates a source elaboration failure.

The checks validate frozen denominators, required node fields, typed reciprocal
proof edges, adjacency, proof-DAG reachability, recipe coverage, source hashes,
hygiene, and the exact conditional root composition. They do not prove
`RadiusSquaredObstruction`, close the root, establish H0/R0, or satisfy any
release gate. Master acceptance is still required.
