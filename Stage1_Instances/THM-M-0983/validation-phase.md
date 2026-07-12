# THM-M-0983 validation phase

Item: `S56-M-0983-VALIDATION`. Base revision:
`8079a8a9396157a95ec61c2b3d868e7cca33e7cd`.

Validation ran in the worker clone on 2026-07-12. It reused the canonical
pinned Lake artifacts and did not update, build, fetch, clone, or otherwise
mutate `.lake`. The exact proof root and a separately implemented reconstruction
of the exact frozen target both reached the Lean kernel. Their `#print axioms`
outputs contained only `propext`, `Classical.choice`, and `Quot.sound`.

```text
python3 Stage1_Instances/THM-M-0983/check_validation.py
  exit 0
  exact proof root and independently reconstructed exact target kernel-replayed
  frozen hashes, denominator, structured recipe, placeholder policy, and clean
  pinned mathlib revision passed

cd Stage1_Instances/THM-M-0983
BASE_LEAN_PATH="$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)"
LEAN_PATH="$BASE_LEAN_PATH" ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 \
  lake env lean -o Statement.olean Statement.lean
LEAN_PATH=".:$BASE_LEAN_PATH" ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 \
  lake env lean -o ObligationTree.olean ObligationTree.lean
LEAN_PATH=".:$BASE_LEAN_PATH" ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 \
  lake env lean Proof.lean
LEAN_PATH=".:$BASE_LEAN_PATH" ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 \
  lake env lean Validation.lean
rm -f Statement.olean ObligationTree.olean
  combined exit 0
  all printed proof and validation declarations depend only on
  [propext, Classical.choice, Quot.sound]

python3 Stage1_Instances/THM-M-0983/check_proof.py
python3 Stage1_Instances/THM-M-0983/check_obligation_tree.py
python3 Docs/tools/check_stage1_standard.py
python3 scripts/stage1_target.py check
python3 scripts/stage1_target.py show THM-M-0983
git diff --check -- Stage1_Instances/THM-M-0983 .stage1-worker-selftest.json
  all exit 0
```

The pinned environment was Lean 4.29.0 commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740` and mathlib commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The terminal upstream declaration
is `ProbabilityTheory.strong_law_ae_real` in
`Mathlib/Probability/StrongLaw.lean`; that source has SHA-256
`b74c93434df44eb75b2567f43a58b9e0353138660ad07b99263d8019bcf4f1c6`.

This is truthful nonrelease validation, not full rev-5.6 release evidence. The
frozen typed graph predates proof closure and still records M3; master
reconciliation is required. Cold empty-cache/offline replay, complete
transitive provenance and TCB/SBOM evidence, accepted H0/R0 reviews, signed
attestations, and a distinct independently provisioned verifier remain open.
Therefore this worker does not claim E0/E1, M0, audit completion, theorem
completion, release, or master acceptance.
