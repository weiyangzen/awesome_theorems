import «Stage1_Instances».«THM-M-1133».Proof
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-1133 validation probe

This module checks that the proof-phase declaration has exactly the frozen
weak heat-equation maximum-principle type. It deliberately adds no second
mathematical proof: importing `Proof` makes this an exact-type replay, not
distinct-runner independent verification.
-/

noncomputable section

namespace Stage1Instances.THM_M_1133.Validation

open Stage1Instances.THM_M_1133

/-- Import-dependent exact-type probe for the repo-local proof root. -/
theorem exactRootProbe : HeatEquationWeakMaximumPrinciple :=
  heatEquationWeakMaximumPrinciple

#check exactRootProbe

assert_no_sorry caloric_isSubcaloric
assert_no_sorry root_of_subsolutionMaximumPrinciple
assert_no_sorry second_deriv_nonpos_of_localMax
assert_no_sorry iteratedFDeriv_diag_nonpos_of_localMax
assert_no_sorry spatialLaplacian_nonpos_of_localMax
assert_no_sorry deriv_nonneg_of_isLocalMaxOn_Iic
assert_no_sorry strictSubsolutionMaximumPrinciple
assert_no_sorry perturb_isStrictSubcaloric
assert_no_sorry weakSubsolutionMaximumPrinciple
assert_no_sorry heatEquationWeakMaximumPrinciple
assert_no_sorry exactRootProbe

#print sorries caloric_isSubcaloric
#print sorries root_of_subsolutionMaximumPrinciple
#print sorries second_deriv_nonpos_of_localMax
#print sorries iteratedFDeriv_diag_nonpos_of_localMax
#print sorries spatialLaplacian_nonpos_of_localMax
#print sorries deriv_nonneg_of_isLocalMaxOn_Iic
#print sorries strictSubsolutionMaximumPrinciple
#print sorries perturb_isStrictSubcaloric
#print sorries weakSubsolutionMaximumPrinciple
#print sorries heatEquationWeakMaximumPrinciple
#print sorries exactRootProbe

#print axioms exactRootProbe

end Stage1Instances.THM_M_1133.Validation
