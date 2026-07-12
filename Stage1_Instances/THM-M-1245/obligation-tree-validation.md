# THM-M-1245 obligation-tree validation

Item: `S56-M-1245-OBLIGATION_TREE`. Base revision:
`c37f5c9477ecee2c5ecf444e75e52be738eff1a8`.

Validation ran from the worker clone on 2026-07-12. Existing pinned Lake
artifacts were reused; no dependency update, fetch, clone, or build was run.

```text
python3 Stage1_Instances/THM-M-1245/build_obligation_artifacts.py
  exit 0
  8783256cbfa268af4fdc511af35ce2f0cbb3229bc3e4469cf558fcd20ef95e12

python3 Stage1_Instances/THM-M-1245/check_obligation_tree.py
  exit 0
  PASS THM-M-1245 obligation tree: 9 obligations, 19 typed edges
  registry denominator sha256: 8783256cbfa268af4fdc511af35ce2f0cbb3229bc3e4469cf558fcd20ef95e12
  root closure: open (M1); named terminal integration belongs to the proof node

cd Stage1_Instances/THM-M-1245 &&
  LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    lake env lean -o Statement.olean Statement.lean &&
  LEAN_PATH=.:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    lake env lean ObligationTree.lean
  exit 1
  error: no default toolchain configured

cd Stage1_Instances/THM-M-1245 &&
  LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    /home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean \
      -o Statement.olean Statement.lean &&
  LEAN_PATH=.:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    /home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean \
      ObligationTree.lean
  exit 0
  root_of_audited_terminal_estimate depends on axioms:
    [propext, Classical.choice, Quot.sound]
  Statement.olean removed after the scoped check.

python3 -m json.tool Stage1_Instances/THM-M-1245/{obligation-registry,typed-graphs,validation-specs}.json
  run separately for each file; all exit 0
python3 Docs/tools/check_stage1_standard.py
  exit 0; 15 assurance groups and 1546 uniform-L0 targets
python3 scripts/stage1_target.py check
  exit 0; 1546 unique targets, ranks 1 through 1546
python3 scripts/stage1_target.py show THM-M-1245
  exit 0; rank 326, planned, theorem_complete false
prohibited-token scan of ObligationTree.lean
  exit 0; no sorry, admit, axiom declaration, sorryAx, or unsafe marker
generated-olean absence check under the owned path
  exit 0; no generated .olean remains
git diff --check -- Stage1_Instances/THM-M-1245
  exit 0; no output
```

The failed `lake env lean` invocation is retained as evidence. Lake exposes the
pinned dependency environment and exact Lean executable, but this clone has no
Elan default. The successful retry uses that installed Lean 4.29.0 binary and
the same Lake-derived `LEAN_PATH`; it does not mutate `.lake`.

These checks validate source hashes, frozen denominators, eligibility lists,
node ledgers, reciprocal typed proof edges, graph adjacency, DAG reachability,
validation recipe coverage, hygiene, elaboration, and the conditional
composition's axiom surface. The terminal candidate is not installed as the
named root proof in this phase. Primary-source H0, trust/provenance closure,
proof acceptance, hermetic replay, independent validation, and theorem
completion remain open. There is no accepted receipt; master acceptance is
still required.
