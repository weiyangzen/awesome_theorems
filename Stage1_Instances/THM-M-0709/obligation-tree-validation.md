# THM-M-0709 obligation-tree validation

Item: `S56-M-0709-OBLIGATION_TREE`. Base revision:
`3a479c703900e8096e6b239e7bf5b0da25472b8a`.

Validation ran in the worker clone on 2026-07-12. Existing pinned Lake
artifacts were reused; no update, build, fetch, clone, or `.lake` mutation was
performed.

```text
python3 Stage1_Instances/THM-M-0709/build_obligation_artifacts.py
  exit 0
  f3731049c66ed6cf5e4687115b723249d54dae577f83859e130b76911f519b38

python3 Stage1_Instances/THM-M-0709/check_obligation_tree.py
  exit 0
  PASS THM-M-0709 obligation tree: 18 obligations, 81 typed edges
  registry denominator sha256: f3731049c66ed6cf5e4687115b723249d54dae577f83859e130b76911f519b38
  root closure: open (M3); the halting-to-binary-PCP reduction remains unimplemented

(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0709/Statement.lean)
  exit 0
  exact target prints as not ComputablePred HasSolution

(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0709/ObligationTree.lean)
  exit 0
  root_interface has the exact root input and output type
  axioms: [propext, Classical.choice, Quot.sound]

python3 Docs/tools/check_stage1_standard.py
  exit 0; 15 assurance groups and 1546 uniform-L0 targets
python3 scripts/stage1_target.py check
  exit 0; 1546 unique targets, ranks 1..1546
python3 scripts/stage1_target.py show THM-M-0709
  exit 0; rank 750, planned, theorem_complete false
python3 -m json.tool <each of obligation-registry.json, typed-graphs.json, validation-specs.json>
  exit 0 for all three structured artifacts
rg -n --glob '*.lean' '\b(sorry|admit|axiom)\b|sorryAx' Stage1_Instances/THM-M-0709
  exit 1 with no matches (expected clean scan)
git diff --check -- Stage1_Instances/THM-M-0709
  exit 0; no whitespace errors
```

The first attempted direct elaboration of `ObligationTree.lean` imported the
unbuilt sibling module `Statement` and failed because this dossier is outside
the Lake source tree. The corrected standalone probe repeats the exact frozen
definitions; `check_statement.py` and the registry source hash guard agreement
with `Statement.lean`. No generated `.olean` or dependency artifact was needed.

The structural checker recomputes source-freeze hashes and the immutable
denominator, checks all required node fields and budgets, verifies typed graph
adjacency, reciprocal proof edges, proof-DAG acyclicity and reachability, and
checks structured validation-recipe coverage. Lean checks only the statement
and exact-root identity interface. It does not check a PCP reduction, any child
composition, primary-source closure, or theorem completion. Master acceptance
remains required.
