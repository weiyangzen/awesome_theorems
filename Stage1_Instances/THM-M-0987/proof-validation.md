# THM-M-0987 proof-phase validation

Item: `S56-M-0987-PROOF`. Base revision:
`6607e765f4b1b664fa13d7035af8e18567eaf062`.

`Proof.lean` supplies a placeholder-free body for the exact
`CentralLimitTheoremTarget` frozen in `Statement.lean`. It also discharges the
frozen `PinnedBridge` and composes that body through `root_of_pinnedBridge` to
the obligation tree's `CanonicalRoot`. Both bodies apply the terminal theorem
`ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub` from the pinned
mathlib dependency; no hypothesis, binder, domain, or zero-variance case is
removed.

Validation ran in the worker clone on 2026-07-12. Existing canonical pinned
Lake artifacts were reused; no update, build, fetch, clone, or dependency
mutation was performed.

```text
cd Stage1_Instances/THM-M-0987
BASE_LEAN_PATH="$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)"
LEAN_PATH="$BASE_LEAN_PATH" ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 \
  lake env lean -o Statement.olean Statement.lean
LEAN_PATH=".:$BASE_LEAN_PATH" ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 \
  lake env lean -o ObligationTree.olean ObligationTree.lean
LEAN_PATH=".:$BASE_LEAN_PATH" ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 \
  lake env lean Proof.lean
rm -f Statement.olean ObligationTree.olean
  combined exit 0
  centralLimitTheorem_proof axioms: [propext, Classical.choice, Quot.sound]
  pinnedBridge_proof axioms: [propext, Classical.choice, Quot.sound]
  canonicalRoot_proof axioms: [propext, Classical.choice, Quot.sound]

python3 Stage1_Instances/THM-M-0987/check_proof.py
  exit 0: PASS; exact root and pinned bridge bodies present
python3 Stage1_Instances/THM-M-0987/check_obligation_tree.py
  exit 0: PASS; 20 frozen obligations and 36 typed edges
python3 Docs/tools/check_stage1_standard.py
  exit 0: ok; 15 assurance groups and 1546 uniform-L0 targets
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-0987
  exit 0: rank 267, planned, theorem_complete false
sha256sum Stage1_Instances/THM-M-0987/{Statement.lean,ObligationTree.lean,Proof.lean}
  4ac6a7cdb7139df6bca2f3eb6b0e211c4ff108ab89b1b99d60186dde75734363  Statement.lean
  3a0d90a9b7416c358948645a6af20490e6273fda37c7f096b2e6de59d4fdb383  ObligationTree.lean
  234794e150172dc78b5fe2534150918151500bff7446ff44365df1c22ba486ae  Proof.lean
git diff --check -- Stage1_Instances/THM-M-0987
  exit 0
```

Pinned environment: Lean `4.29.0` commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib manifest revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`.

The obligation-tree check intentionally reports its immutable pre-proof
closure boundary (`M3`, pinned bridge open). This proof node supplies precisely
that body but does not rewrite earlier phase artifacts. Full transitive trust
and provenance, hermetic replay, independent verification, H/R acceptance,
validation/release nodes, master acceptance, and theorem completion remain
downstream.
