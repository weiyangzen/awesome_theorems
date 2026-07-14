import Statement
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0593 same-worker validation probe

This module imports neither `Proof` nor `ObligationTree`. It independently
spells the exact frozen root, reconstructs the zero-codomain branch, and
checks the exhaustive conditional branch composition. The low-dimensional
and hard Morse-Sard branches remain explicit inputs, so this is not an
unconditional proof of Sard's theorem or a distinct-runner attestation.
-/

namespace Stage1Instances.THMM0593.Validation

open MeasureTheory Set

/-- An independently spelled copy of the canonical proposition. -/
def ExactRoot : Prop :=
  ∀ (m n : ℕ) (f : EuclideanSpace ℝ (Fin m) → EuclideanSpace ℝ (Fin n))
      (R : Set (EuclideanSpace ℝ (Fin m))),
    IsOpen R → ContDiffOn ℝ (⊤ : ℕ∞) f R →
      (volume : Measure (EuclideanSpace ℝ (Fin n)))
        (f '' Stage1Instances.THMM0593.criticalPointsOn f R) = 0

theorem exactRoot_iff_frozen :
    ExactRoot ↔ Stage1Instances.THMM0593.SardTarget :=
  Iff.rfl

def ValidationZeroCodomainBranch : Prop :=
  ∀ (m : ℕ) (f : EuclideanSpace ℝ (Fin m) → EuclideanSpace ℝ (Fin 0))
      (R : Set (EuclideanSpace ℝ (Fin m))),
    IsOpen R → ContDiffOn ℝ (⊤ : ℕ∞) f R →
      (volume : Measure (EuclideanSpace ℝ (Fin 0)))
        (f '' Stage1Instances.THMM0593.criticalPointsOn f R) = 0

def ValidationLowDimensionBranch : Prop :=
  ∀ (m n : ℕ) (f : EuclideanSpace ℝ (Fin m) → EuclideanSpace ℝ (Fin n))
      (R : Set (EuclideanSpace ℝ (Fin m))),
    m < n → IsOpen R → ContDiffOn ℝ (⊤ : ℕ∞) f R →
      (volume : Measure (EuclideanSpace ℝ (Fin n)))
        (f '' Stage1Instances.THMM0593.criticalPointsOn f R) = 0

def ValidationHardDimensionBranch : Prop :=
  ∀ (m n : ℕ) (f : EuclideanSpace ℝ (Fin m) → EuclideanSpace ℝ (Fin n))
      (R : Set (EuclideanSpace ℝ (Fin m))),
    0 < n → n ≤ m → IsOpen R → ContDiffOn ℝ (⊤ : ℕ∞) f R →
      (volume : Measure (EuclideanSpace ℝ (Fin n)))
        (f '' Stage1Instances.THMM0593.criticalPointsOn f R) = 0

/-- A separately implemented proof of the elementary zero-codomain branch. -/
theorem zeroCodomainBranch_validation : ValidationZeroCodomainBranch := by
  intro m f R _hopen _hsmooth
  have hcrit : Stage1Instances.THMM0593.criticalPointsOn f R = ∅ := by
    ext x
    simp only [Stage1Instances.THMM0593.criticalPointsOn, mem_setOf_eq,
      mem_empty_iff_false, iff_false]
    intro hx
    exact hx.2 (Function.surjective_to_subsingleton (fderiv ℝ f x))
  simp [hcrit]

/-- Independent exact-type reconstruction of the three-way composition.

The two analytic branches are premises. In particular, this declaration does
not construct `ValidationHardDimensionBranch` and does not close `ExactRoot`.
-/
theorem conditionalExactRoot
    (low : ValidationLowDimensionBranch)
    (hard : ValidationHardDimensionBranch) : ExactRoot := by
  intro m n f R hopen hsmooth
  by_cases hn : n = 0
  · subst n
    exact zeroCodomainBranch_validation m f R hopen hsmooth
  by_cases hmn : m < n
  · exact low m n f R hmn hopen hsmooth
  · exact hard m n f R (Nat.pos_of_ne_zero hn) (Nat.le_of_not_gt hmn) hopen hsmooth

assert_no_sorry exactRoot_iff_frozen
assert_no_sorry zeroCodomainBranch_validation
assert_no_sorry conditionalExactRoot

#print sorries exactRoot_iff_frozen
#print sorries zeroCodomainBranch_validation
  conditionalExactRoot

#print axioms exactRoot_iff_frozen
#print axioms zeroCodomainBranch_validation
#print axioms conditionalExactRoot

end Stage1Instances.THMM0593.Validation
