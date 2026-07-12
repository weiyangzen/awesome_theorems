# THM-M-1537 obligation-tree validation

Item: `S56-M-1537-OBLIGATION_TREE`. Base revision:
`937d8467b6060fe4128f6ddd0b930b16ba7bd6e6`.

Validation ran in the worker clone on 2026-07-12. Existing pinned Lake artifacts were reused. No
dependency update, fetch, clone, or build was run.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: ok; 15 assurance groups, 1546 uniform-L0 Lean 4 targets

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-1537
  exit 0: execution rank 200; L0/rework_required; planned; theorem_complete false

python3 Stage1_Instances/THM-M-1537/build_obligation_artifacts.py
  exit 0
  generated 9 obligations; denominator
  8c57fc2c6fdba40bd4293e06ca656fbe2cc371cbe00d7ac34528108b2fb13c19

python3 Stage1_Instances/THM-M-1537/check_obligation_tree.py
  exit 0
  PASS THM-M-1537 obligation tree: 9 obligations, 16 typed edges
  registry denominator sha256: 8c57fc2c6fdba40bd4293e06ca656fbe2cc371cbe00d7ac34528108b2fb13c19
  root closure: blocked (M5); canonical target is refuted by a checked model witness

cd Stage1_Instances/THM-M-1537 &&
  LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    lake env lean -o Statement.olean Statement.lean &&
  LEAN_PATH=.:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    lake env lean ObligationTree.lean
  exit 1: no default toolchain configured

cd Stage1_Instances/THM-M-1537 &&
  LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    /home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean \
      -o Statement.olean Statement.lean &&
  LEAN_PATH=.:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
    /home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean \
      ObligationTree.lean
  exit 0
  areaLaw_of_bridge axioms: [propext, Classical.choice, Quot.sound]
  not_bekensteinHawkingAreaLaw axioms: [propext, Classical.choice, Quot.sound]
  Statement.olean removed after the scoped check
```

The failed direct invocation is retained. Lake supplies the pinned dependency environment, but the
clone has no Elan default; the successful retry uses the installed pinned Lean 4.29.0 executable
and the same Lake-derived `LEAN_PATH`.

These checks validate input hashes, frozen denominators, eligibility projections, complete node
ledgers, all seven typed graphs, reciprocal proof edges, adjacency, validation recipe coverage,
placeholder hygiene, exact elaboration, conditional composition, and the countermodel proof. They
do not prove the root. On the contrary, `not_bekensteinHawkingAreaLaw` proves that the universal
target is false for the frozen record because entropy is unconstrained. The obligation-tree phase
is self-tested; proof execution remains blocked pending an authorized model/statement repair and
renewed upstream gates. Master acceptance is still required.
