import «Stage1_Instances».«THM-M-1518».Proof
import «Stage1_Instances».«THM-M-1518».WeakToPointwise

/-!
# THM-M-1518: exact proof assembly

This module composes the checked first-variation and weak-to-pointwise
packages into the exact statement frozen at intake.
-/

noncomputable section

namespace Stage1Instances.THM_M_1518

/-- Exact proof of the stationary-action Euler-Lagrange target. -/
theorem stationaryActionEulerLagrange : StationaryActionEulerLagrangeTarget :=
  ObligationTree.exactTarget_of_packages
    firstVariationFormula ObligationTree.weakToPointwise

#check stationaryActionEulerLagrange
#print axioms stationaryActionEulerLagrange

end Stage1Instances.THM_M_1518
