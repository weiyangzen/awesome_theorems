import Proof
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-1244 kernel-facing proof audit

This module asks Lean to recursively inspect the frozen target transport,
composition boundary, vendored terminal theorem, local packages, and exact root
for `sorryAx`, then prints their complete axiom closures.
-/

open Stage1Instances.THM_M_1244

assert_no_sorry gaussianLogSobolevTarget_iff_expandedTarget
assert_no_sorry gaussianLogSobolevTarget_of_packages
assert_no_sorry GaussianLSI.gaussian_logSobolev_W12_pi
assert_no_sorry coordinateLogSobolevPackage
assert_no_sorry coordinateToOperatorEnergyPackage
assert_no_sorry gaussianLogSobolev

#print sorries gaussianLogSobolevTarget_iff_expandedTarget
#print sorries gaussianLogSobolevTarget_of_packages
#print sorries GaussianLSI.gaussian_logSobolev_W12_pi
#print sorries coordinateLogSobolevPackage
#print sorries coordinateToOperatorEnergyPackage
#print sorries gaussianLogSobolev

#print axioms gaussianLogSobolevTarget_iff_expandedTarget
#print axioms gaussianLogSobolevTarget_of_packages
#print axioms GaussianLSI.gaussian_logSobolev_W12_pi
#print axioms coordinateLogSobolevPackage
#print axioms coordinateToOperatorEnergyPackage
#print axioms gaussianLogSobolev
