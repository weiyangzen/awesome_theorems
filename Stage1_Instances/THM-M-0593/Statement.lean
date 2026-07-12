import Mathlib.Geometry.Euclidean.Volume.Measure
import Mathlib.Analysis.Calculus.ContDiff.Defs

namespace Stage1Instances.THMM0593

open MeasureTheory Set

/-- Points of a region where a Euclidean map has nonsurjective derivative. -/
def criticalPointsOn {m n : ℕ}
    (f : EuclideanSpace ℝ (Fin m) → EuclideanSpace ℝ (Fin n))
    (R : Set (EuclideanSpace ℝ (Fin m))) :
    Set (EuclideanSpace ℝ (Fin m)) :=
  {x | x ∈ R ∧ ¬Function.Surjective (fderiv ℝ f x)}

/--
The smooth Euclidean-region form of Sard's theorem: the critical values of a smooth map from an
open region of `ℝ^m` to `ℝ^n` have `n`-dimensional Lebesgue measure zero.
-/
def SardTarget : Prop :=
  ∀ (m n : ℕ) (f : EuclideanSpace ℝ (Fin m) → EuclideanSpace ℝ (Fin n))
      (R : Set (EuclideanSpace ℝ (Fin m))),
    IsOpen R → ContDiffOn ℝ (⊤ : ℕ∞) f R →
      (volume : Measure (EuclideanSpace ℝ (Fin n))) (f '' criticalPointsOn f R) = 0

#check SardTarget

end Stage1Instances.THMM0593
