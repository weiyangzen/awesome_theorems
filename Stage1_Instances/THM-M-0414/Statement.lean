import Mathlib.RingTheory.DedekindDomain.Factorization

/-!
# THM-M-0414: exact unique factorization statement for ideals

This module freezes and tests the statement boundary only. It does not claim
proof completion for the theorem dossier.
-/

noncomputable section

namespace Stage1Instances.THM_M_0414

universe u

/-- The canonical target: ideals of a Dedekind domain have unique
factorization, and every nonzero ideal has the explicit finite product over
its height-one prime factors. The unit ideal is included as the empty-product
case. -/
def IdealUniqueFactorizationTarget : Prop :=
  ∀ (R : Type u) [CommRing R] [IsDedekindDomain R],
    UniqueFactorizationMonoid (Ideal R) ∧
      ∀ {I : Ideal R}, I ≠ 0 →
        ∏ᶠ v : IsDedekindDomain.HeightOneSpectrum R, v.maxPowDividing I = I

/-- Direct local transcription of the historical candidate statement. -/
def HistoricalCandidateShape : Prop :=
  ∀ (R : Type u) [CommRing R] [IsDedekindDomain R],
    UniqueFactorizationMonoid (Ideal R) ∧
      ∀ {I : Ideal R}, I ≠ 0 →
        ∏ᶠ v : IsDedekindDomain.HeightOneSpectrum R, v.maxPowDividing I = I

/-- Checked identity between the canonical target and the historical shape.
The historical declaration remains discovery input rather than proof credit. -/
theorem idealUniqueFactorizationTarget_iff_historicalCandidateShape :
    IdealUniqueFactorizationTarget.{u} ↔ HistoricalCandidateShape.{u} :=
  Iff.rfl

-- Separately elaborated structural mutations used by `check_statement.py`.
def mutationRemovedNonzeroHypothesis : Prop :=
  ∀ (R : Type u) [CommRing R] [IsDedekindDomain R],
    UniqueFactorizationMonoid (Ideal R) ∧
      ∀ I : Ideal R,
        ∏ᶠ v : IsDedekindDomain.HeightOneSpectrum R, v.maxPowDividing I = I

def mutationChangedDomainToIntegers : Prop :=
  UniqueFactorizationMonoid (Ideal ℤ) ∧
    ∀ {I : Ideal ℤ}, I ≠ 0 →
      ∏ᶠ v : IsDedekindDomain.HeightOneSpectrum ℤ, v.maxPowDividing I = I

def mutationChangedBinderScope : Prop :=
  ∀ (R : Type u) [CommRing R] [IsDedekindDomain R],
    (∀ I : Ideal R, I ≠ 0) →
      UniqueFactorizationMonoid (Ideal R) ∧
        ∀ I : Ideal R,
          ∏ᶠ v : IsDedekindDomain.HeightOneSpectrum R, v.maxPowDividing I = I

def mutationExcludedUnitIdeal : Prop :=
  ∀ (R : Type u) [CommRing R] [IsDedekindDomain R],
    UniqueFactorizationMonoid (Ideal R) ∧
      ∀ {I : Ideal R}, I ≠ 0 → I ≠ ⊤ →
        ∏ᶠ v : IsDedekindDomain.HeightOneSpectrum R, v.maxPowDividing I = I

/-- The unit ideal is deliberately in scope. This kernel check exercises its
empty-product boundary through the selected mathlib formulation. -/
theorem unitIdealBoundary (R : Type u) [CommRing R] [IsDedekindDomain R] :
    ∏ᶠ v : IsDedekindDomain.HeightOneSpectrum R,
        v.maxPowDividing (⊤ : Ideal R) = ⊤ := by
  apply Ideal.finprod_heightOneSpectrum_factorization
  exact (top_ne_bot : (⊤ : Ideal R) ≠ ⊥)

end Stage1Instances.THM_M_0414

set_option pp.explicit true in
#print Stage1Instances.THM_M_0414.IdealUniqueFactorizationTarget
