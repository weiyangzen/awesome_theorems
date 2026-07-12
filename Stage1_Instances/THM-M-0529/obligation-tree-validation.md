# THM-M-0529 obligation-tree validation

Item: `S56-M-0529-OBLIGATION_TREE`  
Base revision: `9a5088a76a8219c7df161c5dbaeb2de32d6ce742`  
Run date: 2026-07-12

The registry freezes seven unique obligations and separate proof, refinement, provenance, evidence,
trust, documentation, and workflow graphs. The proof DAG contains the exact root, a checked
conditional map-composition certificate, and the two substantive pinned-mathlib bridges. Every
semantic ledger has a 20-step budget. Statement, primary-source, and provenance requirements are
separate overlays and cannot inflate proof-body coverage.

Validation reused only the existing pinned Lake artifacts. No update, build, clone, fetch, or other
dependency mutation was performed.

```text
python3 Stage1_Instances/THM-M-0529/build_obligation_artifacts.py
  exit 0
  86fd370d7c5af8729480b1ef9d0e1fb0a294a84f46d1d711aa2af5c2cec0c3b5

python3 Stage1_Instances/THM-M-0529/check_obligation_tree.py
  exit 0
  PASS THM-M-0529 obligation tree: 7 obligations, 15 typed edges
  registry denominator sha256: 86fd370d7c5af8729480b1ef9d0e1fb0a294a84f46d1d711aa2af5c2cec0c3b5
  root closure: open (M3); proof-phase bridge acceptance and provenance remain open

cd Formalizations/Lean &&
  lake env lean ../../Stage1_Instances/THM-M-0529/ObligationTree.lean
  exit 0
  TopCat.isoOfHomeo and CategoryTheory.Functor.map_isIso resolved.
  map_isIso_of_source_isIso depends on [propext, Classical.choice, Quot.sound].

cd Formalizations/Lean &&
  lake env lean ../../Stage1_Instances/THM-M-0529/Statement.lean
  exit 0
  AwesomeTheorems.THM_M_0529.CanonicalTarget re-elaborated unchanged.

python3 Docs/tools/check_stage1_standard.py
  exit 0
  15 assurance groups and 1546 uniform-L0 Lean 4 targets passed.

python3 scripts/stage1_target.py check
  exit 0
  1546 unique targets, ranks 1..1546, all L0/rework_required.

python3 scripts/stage1_target.py show THM-M-0529
  exit 0
  rank 586; planned; theorem_complete false.

git diff --check -- Stage1_Instances/THM-M-0529
  exit 0; no output.
```

The structural checker verifies input hashes, denominator recomputation, eligibility projections,
unique IDs, all required node fields, `<=100` budgets, typed graph adjacency, reciprocal proof and
composition edges, proof-DAG reachability, structured validation recipe coverage, source hygiene,
and the deliberately open closure boundary.

This node freezes architecture; it does not accept the later proof node. The root remains `M3`,
with no `H0`, `R0`, audit completion, theorem completion, or master receipt claimed.
