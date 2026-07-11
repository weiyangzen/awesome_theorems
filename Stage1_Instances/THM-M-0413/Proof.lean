import Mathlib.NumberTheory.NumberField.Basic

/-!
Proof-phase kernel certificates for THM-M-0413.

The root certificate deliberately names the pinned generic integral-closure theorem used by
mathlib's number-field instance.  The component certificates expose the four fields assembled by
that theorem, so the proof is not credited merely from an opaque typeclass search.
-/

namespace Stage1.THMM0413.Proof

universe u

open scoped NumberField

abbrev O (K : Type u) [Field K] := NumberField.RingOfIntegers K

/-- The domain component is inherited from the integral closure's subtype construction. -/
theorem domainComponent (K : Type u) [Field K] [NumberField K] : IsDomain (O K) :=
  inferInstance

/-- Noetherianity is the finite-separable integral-closure theorem specialized to `Z`, `Q`, `K`. -/
theorem noetherianComponent (K : Type u) [Field K] [NumberField K] :
    IsNoetherianRing (O K) :=
  IsIntegralClosure.isNoetherianRing ℤ ℚ K (O K)

/-- Dimension at most one is preserved by this integral closure. -/
theorem dimensionComponent (K : Type u) [Field K] [NumberField K] :
    Ring.DimensionLEOne (O K) :=
  Ring.DimensionLEOne.isIntegralClosure ℤ K (O K)

/-- Integral closedness is the corresponding field-of-fractions characterization. -/
theorem integralClosedComponent (K : Type u) [Field K] [NumberField K] :
    IsIntegrallyClosed (O K) := by
  letI : IsFractionRing (O K) K :=
    IsIntegralClosure.isFractionRing_of_finite_extension ℤ ℚ K (O K)
  rw [isIntegrallyClosed_iff K]
  intro x hx
  exact
    ⟨IsIntegralClosure.mk' (O K) x (isIntegral_trans (R := ℤ) _ hx),
      IsIntegralClosure.algebraMap_mk' _ _ _⟩

/-- Explicit assembly of the four defining components into the exact target. -/
theorem fromComponents (K : Type u) [Field K] [NumberField K] :
    IsDedekindDomain (O K) :=
  @IsDedekindDomain.mk _ _ (domainComponent K)
    (@IsDedekindRing.mk _ _ (noetherianComponent K) (dimensionComponent K)
      (integralClosedComponent K))

/-- Exact root certificate, using the pinned terminal proof body rather than instance synthesis. -/
theorem exactRoot :
    ∀ (K : Type u) [Field K] [NumberField K], IsDedekindDomain (O K) := by
  intro K _ _
  exact IsIntegralClosure.isDedekindDomain ℤ ℚ K (O K)

/-- Independent local assembly agrees at the proposition level with the terminal route. -/
theorem exactRootFromComponents :
    ∀ (K : Type u) [Field K] [NumberField K], IsDedekindDomain (O K) := by
  intro K _ _
  exact fromComponents K

#check exactRoot
#check exactRootFromComponents
#print axioms domainComponent
#print axioms noetherianComponent
#print axioms dimensionComponent
#print axioms integralClosedComponent
#print axioms exactRoot
#print axioms exactRootFromComponents

end Stage1.THMM0413.Proof
