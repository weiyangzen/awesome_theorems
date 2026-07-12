import Mathlib.Geometry.Euclidean.Volume.Measure
import Mathlib.Analysis.Calculus.ContDiff.Defs

namespace Stage1Instances.THMM0593

open MeasureTheory Set

def criticalPointsOn {m n : ℕ}
    (f : EuclideanSpace ℝ (Fin m) → EuclideanSpace ℝ (Fin n))
    (R : Set (EuclideanSpace ℝ (Fin m))) : Set (EuclideanSpace ℝ (Fin m)) :=
  {x | x ∈ R ∧ ¬Function.Surjective (fderiv ℝ f x)}

def SardTarget : Prop :=
  ∀ (m n : ℕ) (f : EuclideanSpace ℝ (Fin m) → EuclideanSpace ℝ (Fin n))
      (R : Set (EuclideanSpace ℝ (Fin m))),
    IsOpen R → ContDiffOn ℝ (⊤ : ℕ∞) f R →
      (volume : Measure (EuclideanSpace ℝ (Fin n))) (f '' criticalPointsOn f R) = 0

example (h : SardTarget) :
    ∀ (m n : ℕ) (f : EuclideanSpace ℝ (Fin m) → EuclideanSpace ℝ (Fin n))
      (R : Set (EuclideanSpace ℝ (Fin m))), ContDiffOn ℝ (⊤ : ℕ∞) f R →
        (volume : Measure (EuclideanSpace ℝ (Fin n))) (f '' criticalPointsOn f R) = 0 := by
  unfold SardTarget at h
  intro m n f R hf
  exact h m n f R

end Stage1Instances.THMM0593
