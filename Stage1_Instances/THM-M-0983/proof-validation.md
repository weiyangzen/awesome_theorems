# THM-M-0983 proof-phase validation

Item: `S56-M-0983-PROOF`. Base revision:
`c648ab4343c997887a2d19de0f3cb93da4f2e10f`.

`Proof.lean` supplies placeholder-free bodies for all three substantive
packages frozen by the obligation tree: family-to-pairwise independence, the
pinned real-valued strong law, and expectation-limit transport. It composes
those packages with `root_of_packages` and separately proves the exact
`BernoulliStrongLawTarget` imported from `Statement.lean`. The `0/1` premise is
kept in the exact target even though mathlib's more general theorem does not
need it.

Validation ran in the worker clone on 2026-07-12. Existing canonical pinned
Lake artifacts were reused; no update, build, fetch, clone, or dependency
mutation was performed.

```text
cd Stage1_Instances/THM-M-0983
BASE_LEAN_PATH="$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)"
LEAN_PATH="$BASE_LEAN_PATH" ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 \
  lake env lean -o Statement.olean Statement.lean
LEAN_PATH=".:$BASE_LEAN_PATH" ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 \
  lake env lean -o ObligationTree.olean ObligationTree.lean
LEAN_PATH=".:$BASE_LEAN_PATH" ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 \
  lake env lean Proof.lean
rm -f Statement.olean ObligationTree.olean
  combined exit 0
  pairwiseProjection_proof axioms: [propext, Classical.choice, Quot.sound]
  strongLaw_proof axioms: [propext, Classical.choice, Quot.sound]
  expectationTransport_proof axioms: [propext, Classical.choice, Quot.sound]
  obligationTarget_proof axioms: [propext, Classical.choice, Quot.sound]
  bernoulliStrongLaw_proof axioms: [propext, Classical.choice, Quot.sound]

python3 Docs/tools/check_stage1_standard.py
  exit 0: ok; 15 assurance groups and 1546 uniform-L0 targets
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-0983
  exit 0: rank 263, planned, theorem_complete false
python3 Stage1_Instances/THM-M-0983/check_proof.py
  exit 0: PASS; three packages and exact root body present
python3 Stage1_Instances/THM-M-0983/check_obligation_tree.py
  exit 0: PASS; 10 frozen obligations and 32 typed edges
sha256sum Stage1_Instances/THM-M-0983/{Statement.lean,ObligationTree.lean,Proof.lean}
  ee2bcf84a0ecabfdecd39b079957f6df58d48bf41ff0485ce8ebf96399f3d871  Statement.lean
  be7500588020e57af35389d4759829a0af415177307fccc54ad2c17d2f2e76cd  ObligationTree.lean
  6834296be8f27073b674a7f004fcbd0da4097af74927ad6e22fc6c97ea9c03dc  Proof.lean
```

Pinned environment: Lean `4.29.0` commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95`.

The obligation-tree check intentionally reports its frozen pre-proof closure
boundary (`M3`, three packages open); this proof node supplies precisely those
three bodies but does not rewrite the earlier phase's immutable artifacts.
Validation, source/readability acceptance, hermetic replay, independent
verification, master acceptance, and theorem completion remain downstream.
