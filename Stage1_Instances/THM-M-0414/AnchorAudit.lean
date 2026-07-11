import Mathlib.RingTheory.DedekindDomain.Factorization

/-!
# THM-M-0414 pinned anchor audit

This module checks the two mathlib declarations that compose the frozen target. It is an audit
adapter only; proof integration belongs to the later proof node.
-/

noncomputable section

namespace Stage1Instances.THM_M_0414

universe u

/-- Audit-local transcription of the exact proposition frozen in `Statement.lean`. -/
def IdealUniqueFactorizationTarget : Prop :=
  ∀ (R : Type u) [CommRing R] [IsDedekindDomain R],
    UniqueFactorizationMonoid (Ideal R) ∧
      ∀ {I : Ideal R}, I ≠ 0 →
        ∏ᶠ v : IsDedekindDomain.HeightOneSpectrum R, v.maxPowDividing I = I

/-- Exact candidate for the frozen target, composed only from the two pinned mathlib anchors. -/
theorem idealUniqueFactorization_mathlib_candidate :
    IdealUniqueFactorizationTarget.{u} := by
  intro R _ _
  exact ⟨inferInstance, fun hI => Ideal.finprod_heightOneSpectrum_factorization hI⟩

#check Ideal.uniqueFactorizationMonoid
#check Ideal.finprod_heightOneSpectrum_factorization
#print axioms Ideal.uniqueFactorizationMonoid
#print axioms Ideal.finprod_heightOneSpectrum_factorization
#print axioms idealUniqueFactorization_mathlib_candidate

end Stage1Instances.THM_M_0414
