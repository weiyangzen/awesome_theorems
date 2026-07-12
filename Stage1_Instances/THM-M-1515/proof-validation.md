# THM-M-1515 proof validation

Item: `S56-M-1515-PROOF`. Base revision:
`6afdcb2c5487434cce7acf7aeb8ed471faf92666`.

The proof phase supplies both open analytic packages from the frozen obligation
tree. `boundary_along_curve_derivative` composes the Frechet derivative of the
boundary with the derivative of the trajectory. `momentum_pairing_derivative`
uses Euler-Lagrange for the momentum covector, the chain rule for the generator,
and the continuous-linear-map application rule. `noether_first_theorem` then
uses the previously checked subtraction composition to prove the exact frozen
target.

Validation ran in the worker clone on 2026-07-12. It reused existing pinned
Lake artifacts and did not update, build, fetch, clone, or otherwise mutate a
dependency.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-1515
  exit 0: rank 184, planned, theorem_complete false

cd Stage1_Instances/THM-M-1515
LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 \
  lake env lean -o Statement.olean Statement.lean
LEAN_PATH=.:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 \
  lake env lean -o ObligationTree.olean ObligationTree.lean
LEAN_PATH=.:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 \
  lake env lean Proof.lean
  combined exit 0
  boundary_along_curve_derivative axioms: [propext, Classical.choice, Quot.sound]
  momentum_pairing_derivative axioms: [propext, Classical.choice, Quot.sound]
  noether_first_theorem axioms: [propext, Classical.choice, Quot.sound]
  generated Statement.olean and ObligationTree.olean removed after the check

sha256sum Stage1_Instances/THM-M-1515/Proof.lean
  exit 0: bab403a8dbb3f4bbfd0b4180190218913640246d2eac233bebfb451acd91552a

git diff --check
  exit 0
```

No placeholder or new axiom is present in the proof source, and the printed
axiom inventory contains no `sorryAx`. This is narrow proof-phase evidence, not
hermetic validation, independent acceptance, audit completion, or theorem
release. Those later nodes remain under master control.
