import «Stage1_Instances».«THM-M-1518».Proof
import «Stage1_Instances».«THM-M-1518».WeakToPointwise
import Mathlib.Util.AssertNoSorry

/-!
# THM-M-1518 differential validation probe

This module deliberately does not import `ExactProof`. It independently
recomposes the two proof packages at the exact frozen target. This is a
same-worker differential composition check, not the distinct signed runner
required for release-grade independent verification.
-/

noncomputable section

namespace Stage1Instances.THM_M_1518.Validation

open Stage1Instances.THM_M_1518

/-- A separately written composition of the checked analytic packages at the
exact target type. -/
theorem independentlyRecomposedStationaryActionEulerLagrange :
    StationaryActionEulerLagrangeTarget := by
  intro n L B q hL hq _ _ hstationary
  apply ObligationTree.weakToPointwise n L B q hL hq
  intro eta heta
  rw [← firstVariationFormula n L B q hL hq eta heta]
  exact hstationary eta heta

#check independentlyRecomposedStationaryActionEulerLagrange
assert_no_sorry firstVariationFormula
assert_no_sorry ObligationTree.weakToPointwise
assert_no_sorry independentlyRecomposedStationaryActionEulerLagrange
#print sorries firstVariationFormula
#print sorries ObligationTree.weakToPointwise
#print sorries independentlyRecomposedStationaryActionEulerLagrange
#print axioms firstVariationFormula
#print axioms ObligationTree.weakToPointwise
#print axioms independentlyRecomposedStationaryActionEulerLagrange

end Stage1Instances.THM_M_1518.Validation
