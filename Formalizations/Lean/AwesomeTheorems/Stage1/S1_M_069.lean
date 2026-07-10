import Mathlib.RingTheory.DedekindDomain.Factorization

/-!
# S1-M-069 / THM-M-0414: unique factorization of ideals in Dedekind domains

This Stage1 artifact records the theorem in the form already available in the
local mathlib pin.  The main wrapper exposes both views used by the classical
statement:

* ideals of a Dedekind domain form a unique factorization monoid;
* every nonzero ideal is the finite product over height-one prime ideals of its
  prime-power components;
* the corresponding nonzero fractional-ideal factorization holds with integer
  exponents given by `FractionalIdeal.count`.

The proof body is supplied by mathlib, not by a repo-local proof developed here.
-/

noncomputable section

open scoped nonZeroDivisors

universe u v

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_069

/-- Stage1 normalized statement for ideal unique factorization in a Dedekind
domain.  The second conjunct is the explicit factorization formula over
height-one prime ideals. -/
def StatementShape : Prop :=
  ∀ (R : Type u) [CommRing R] [IsDedekindDomain R],
    UniqueFactorizationMonoid (Ideal R) ∧
      ∀ {I : Ideal R}, I ≠ 0 →
        ∏ᶠ v : IsDedekindDomain.HeightOneSpectrum R, v.maxPowDividing I = I

/-- Optional Stage1 strengthening: nonzero fractional ideals over the fraction
field of a Dedekind domain factor as a finite product over height-one prime
ideals with integer exponents. -/
def FractionalIdealExtensionShape : Prop :=
  ∀ (R : Type u) [CommRing R] (K : Type v) [Field K] [Algebra R K]
    [IsFractionRing R K] [IsDedekindDomain R],
    ∀ {I : FractionalIdeal R⁰ K}, I ≠ 0 →
      ∏ᶠ v : IsDedekindDomain.HeightOneSpectrum R,
          (v.asIdeal : FractionalIdeal R⁰ K) ^ (FractionalIdeal.count K v I) = I

/-- Mathlib wrapper: ideals of a Dedekind domain form a unique factorization
monoid. -/
theorem ideal_uniqueFactorizationMonoid (R : Type u) [CommRing R] [IsDedekindDomain R] :
    UniqueFactorizationMonoid (Ideal R) := by
  infer_instance

/-- Mathlib wrapper: explicit finite-product factorization of a nonzero ideal
over the height-one prime ideals of a Dedekind domain. -/
theorem ideal_finprod_heightOneSpectrum_factorization {R : Type u} [CommRing R]
    [IsDedekindDomain R] {I : Ideal R} (hI : I ≠ 0) :
    ∏ᶠ v : IsDedekindDomain.HeightOneSpectrum R, v.maxPowDividing I = I :=
  Ideal.finprod_heightOneSpectrum_factorization hI

/-- Mathlib wrapper: only finitely many height-one prime ideals divide a given
nonzero ideal. -/
theorem ideal_finite_factors {R : Type u} [CommRing R] [IsDedekindDomain R]
    {I : Ideal R} (hI : I ≠ 0) :
    {v : IsDedekindDomain.HeightOneSpectrum R | v.asIdeal ∣ I}.Finite :=
  Ideal.finite_factors hI

/-- Mathlib wrapper: explicit finite-product factorization of a nonzero
fractional ideal over the height-one prime ideals of a Dedekind domain. -/
theorem fractionalIdeal_finprod_heightOneSpectrum_factorization {R : Type u}
    [CommRing R] {K : Type v} [Field K] [Algebra R K] [IsFractionRing R K]
    [IsDedekindDomain R] {I : FractionalIdeal R⁰ K} (hI : I ≠ 0) :
    ∏ᶠ v : IsDedekindDomain.HeightOneSpectrum R,
        (v.asIdeal : FractionalIdeal R⁰ K) ^ (FractionalIdeal.count K v I) = I :=
  FractionalIdeal.finprod_heightOneSpectrum_factorization' K hI

/-- The Stage1 statement shape is discharged by the local mathlib wrapper
anchors. -/
theorem statementShape_from_mathlib : StatementShape.{u} := by
  intro R _ _
  exact ⟨ideal_uniqueFactorizationMonoid R, fun hI =>
    ideal_finprod_heightOneSpectrum_factorization hI⟩

/-- The optional fractional-ideal extension shape is discharged by the local
mathlib wrapper anchor. -/
theorem fractionalIdealExtensionShape_from_mathlib :
    FractionalIdealExtensionShape.{u, v} := by
  intro R _ K _ _ _ _ I hI
  exact fractionalIdeal_finprod_heightOneSpectrum_factorization hI

end S1_M_069
end Stage1
end AwesomeTheorems

-- Audit probes for the mathlib anchors wrapped above.
#check IsDedekindDomain
#check IsDedekindDomain.HeightOneSpectrum
#check Ideal.uniqueFactorizationMonoid
#check Ideal.finprod_heightOneSpectrum_factorization
#check Ideal.finite_factors
#check FractionalIdeal.count
#check FractionalIdeal.finprod_heightOneSpectrum_factorization'
#check AwesomeTheorems.Stage1.S1_M_069.StatementShape
#check AwesomeTheorems.Stage1.S1_M_069.statementShape_from_mathlib
#check AwesomeTheorems.Stage1.S1_M_069.FractionalIdealExtensionShape
#check AwesomeTheorems.Stage1.S1_M_069.fractionalIdeal_finprod_heightOneSpectrum_factorization
#check AwesomeTheorems.Stage1.S1_M_069.fractionalIdealExtensionShape_from_mathlib
