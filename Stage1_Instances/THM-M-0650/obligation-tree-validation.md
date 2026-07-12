# THM-M-0650 obligation-tree validation

Item: `S56-M-0650-OBLIGATION_TREE`. Base revision:
`8a4de324e430348fba945ccc31633dc565330377`.

Validation ran in the worker clone on 2026-07-12. It reused the existing pinned
Lake dependency closure and did not update, fetch, clone, or build dependencies.

```text
python3 Stage1_Instances/THM-M-0650/build_obligation_artifacts.py
  exit 0
  wrote 19 obligations and 38 typed edges
  76fcfa12ad9d8f829ca1f7cf79a690badfb720641a5d75376b1925f1f49a3132

python3 Stage1_Instances/THM-M-0650/check_obligation_tree.py
  exit 0
  PASS THM-M-0650 obligation tree: 19 obligations, 38 typed edges
  registry denominator sha256: 76fcfa12ad9d8f829ca1f7cf79a690badfb720641a5d75376b1925f1f49a3132
  root closure: open (M3); pinned embedding body is an uncredited proof-phase candidate

LEAN_BIN=$(cd Formalizations/Lean && lake env which lean)
LEAN_DEPS=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
cd Stage1_Instances/THM-M-0650
LEAN_PATH="$LEAN_DEPS" "$LEAN_BIN" -o Statement.olean Statement.lean
LEAN_PATH=".:$LEAN_DEPS" "$LEAN_BIN" ObligationTree.lean
rm -f Statement.olean Statement.ilean
  exit 0
  root_of_embeddingTarskiVaughtPackage depends on axioms: [Quot.sound]

python3 Docs/tools/check_stage1_standard.py
  exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets
python3 scripts/stage1_target.py check
  exit 0; 1546 unique targets, ranks 1..1546
python3 scripts/stage1_target.py show THM-M-0650
  exit 0; rank 696, planned, theorem_complete false
```

The structural checker recomputes statement and anchor hashes, the canonical
denominator, instance linkage, required node fields, typed reciprocal proof
edges, adjacency, proof-DAG reachability, recipe coverage, closure boundary,
and source hygiene. The Lean check reaches the exact conditional root
composition using the pinned executable and dependency path.

These checks freeze architecture and validate a composition boundary. They do
not credit the candidate embedding proof, close the root, establish H0/R0,
complete transitive provenance or trust, or satisfy any release gate. Master
acceptance is still required.
