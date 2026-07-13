import Statement

/-!
# THM-M-0414 differential validation probe

This module deliberately imports neither `Proof` nor `ObligationTree`. It reconstructs the exact
frozen root directly from the two pinned mathlib declarations, providing a second local proof route
without claiming the distinct runner required for release-grade independent verification.
-/

noncomputable section

namespace Stage1Instances.THM_M_0414.Validation

universe u

/-- A separately written exact-root probe over the same frozen statement. -/
theorem independentExactRoot :
    IdealUniqueFactorizationTarget.{u} := by
  intro R _ _
  exact ⟨Ideal.uniqueFactorizationMonoid,
    fun hI => Ideal.finprod_heightOneSpectrum_factorization hI⟩

#check independentExactRoot
#print axioms independentExactRoot
#print axioms Ideal.uniqueFactorizationMonoid
#print axioms Ideal.finprod_heightOneSpectrum_factorization

end Stage1Instances.THM_M_0414.Validation
