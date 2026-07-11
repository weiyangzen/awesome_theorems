import Statement

/-!
# THM-M-0414 proof bodies

This module integrates the two pinned mathlib terminal bodies and composes them
into the exact statement frozen in `Statement.lean`.
-/

noncomputable section

namespace Stage1Instances.THM_M_0414

universe u

/-- The unique-factorization-monoid component, exposed at its frozen type. -/
theorem idealUniqueFactorizationMonoid_proof
    (R : Type u) [CommRing R] [IsDedekindDomain R] :
    UniqueFactorizationMonoid (Ideal R) :=
  Ideal.uniqueFactorizationMonoid

/-- The explicit finite-product component, with exactly the frozen nonzero
hypothesis and with the unit ideal still in scope. -/
theorem idealFiniteProductFactorization_proof
    {R : Type u} [CommRing R] [IsDedekindDomain R]
    {I : Ideal R} (hI : I ≠ 0) :
    ∏ᶠ v : IsDedekindDomain.HeightOneSpectrum R, v.maxPowDividing I = I :=
  Ideal.finprod_heightOneSpectrum_factorization hI

/-- Closed proof body for the canonical target. -/
theorem idealUniqueFactorizationTarget_proof :
    IdealUniqueFactorizationTarget.{u} := by
  intro R _ _
  exact ⟨idealUniqueFactorizationMonoid_proof R,
    fun hI => idealFiniteProductFactorization_proof hI⟩

#print axioms idealUniqueFactorizationMonoid_proof
#print axioms idealFiniteProductFactorization_proof
#print axioms idealUniqueFactorizationTarget_proof

end Stage1Instances.THM_M_0414
