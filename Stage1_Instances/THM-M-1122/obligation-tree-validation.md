# THM-M-1122 obligation-tree validation

Item: `S56-M-1122-OBLIGATION_TREE`. Base revision: `aa6d10d262275c028256db77ef82b5418d76bc27`.

Validation ran in the worker clone on 2026-07-12 using the existing pinned Lake artifacts. No update,
build, clone, fetch, or other `.lake` mutation was performed.

```text
python3 Stage1_Instances/THM-M-1122/build_obligation_artifacts.py
  exit 0
  1d0de23916fcad958d90c75f413a8446ecb182dd24c412254744500d412863fd

python3 Stage1_Instances/THM-M-1122/check_obligation_tree.py
  exit 0
  PASS THM-M-1122 obligation tree: 11 obligations, 19 typed edges
  registry denominator sha256: 1d0de23916fcad958d90c75f413a8446ecb182dd24c412254744500d412863fd
  root closure: open (M3); ConditionalIdentification remains M4

cd Stage1_Instances/THM-M-1122 &&
  LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    /home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean \
      -o Statement.olean Statement.lean &&
  LEAN_PATH=.:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    /home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean \
      ObligationTree.lean
  exit 0
  root_of_conditionalIdentification depends on axioms:
    [propext, Classical.choice, Quot.sound]
  Statement.olean removed after the scoped check.

python3 Docs/tools/check_stage1_standard.py
  exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets
python3 scripts/stage1_target.py check
  exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-1122
  exit 0; rank 562, planned, theorem_complete false
python3 -m json.tool on obligation-registry.json, typed-graphs.json, and validation-specs.json
  exit 0 for all three files
git diff --check -- Stage1_Instances/THM-M-1122 .stage1-worker-selftest.json
  exit 0; no output
```

The scoped Lean recipe uses the exact already-installed pinned Lean 4.29.0 executable because the
module import requires a temporary sibling `Statement.olean`. `LEAN_PATH` is obtained from the
existing pinned Lake environment; the temporary artifact was deleted. The direct preliminary
attempt to run `ObligationTree.lean` without compiling the sibling module failed with `unknown
module prefix 'Statement'`; it produced no persistent artifact and was corrected by the recorded
scoped recipe above.

These checks cover input hashes, frozen denominators, typed graph adjacency and reciprocal proof
edges, node ledgers and step budgets, validation-recipe coverage, forbidden-placeholder hygiene,
Lean elaboration, and the axiom surface of the conditional composition.

This validates the architecture, not the substantive identification premise. There is no accepted
receipt; master acceptance remains required.
