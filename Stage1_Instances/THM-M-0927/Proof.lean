import ObligationTree
import Mathlib.NumberTheory.Real.GoldenRatio
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0927 proof execution

This module installs pinned mathlib's function-level Binet theorem at the
frozen terminal interface, then consumes every child of the checked
obligation-tree composition to prove the exact radical target.
-/

noncomputable section

namespace Stage1Instances.THM_M_0927.Proof

open Stage1Instances.THM_M_0927

/-- Frozen `M0927-T-FUNCTION-BINET`, supplied by the pinned substantive body
`Real.coe_fib_eq'`. The pointwise wrapper `Real.coe_fib_eq` is deliberately
not counted as a second terminal proof body. -/
theorem functionBinet_proof : ObligationTree.FunctionNamedRootPackage := by
  simpa only [ObligationTree.FunctionNamedRootPackage] using Real.coe_fib_eq'

/-- Checked child-to-parent composition of the pinned function theorem and
both frozen representation transports at the exact statement-phase target. -/
theorem binetFormula_proof : BinetFormulaTarget :=
  ObligationTree.root_of_terminal_packages
    ObligationTree.rootComposition_checked
    functionBinet_proof
    ObligationTree.functionToPointwiseTransport_checked
    ObligationTree.namedRootToRadicalTransport_checked

#check functionBinet_proof
#check binetFormula_proof

#print axioms Real.coe_fib_eq'
#print axioms functionBinet_proof
#print axioms binetFormula_proof

assert_no_sorry Real.coe_fib_eq'
assert_no_sorry functionBinet_proof
assert_no_sorry binetFormula_proof

#print sorries Real.coe_fib_eq'
#print sorries functionBinet_proof
#print sorries binetFormula_proof

end Stage1Instances.THM_M_0927.Proof
