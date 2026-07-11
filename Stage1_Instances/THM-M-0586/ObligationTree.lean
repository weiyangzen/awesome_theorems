import Statement

/-!
# THM-M-0586 conditional obligation composition

This file checks only that complete proofs of the dimension-five and stable
dimension packages compose into the frozen target. It does not prove either
package or the generalized Poincare theorem.
-/

namespace Stage1Instances.THMM0586

universe u

open ContinuousMap
open scoped Manifold ContDiff

/-- The exact boundary branch isolated from the canonical target. -/
def DimensionFivePackage : Prop :=
  forall (M : Type u) [TopologicalSpace M] [T2Space M]
    [ChartedSpace (EuclideanModel 5) M]
    [IsManifold (𝓡 5) ∞ M]
    [CompactSpace M],
      M ≃ₕ UnitSphere 5 -> Nonempty (M ≃ₜ UnitSphere 5)

/-- The dimensions strictly above the lower boundary. -/
def StableDimensionPackage : Prop :=
  forall (n : Nat), 6 <= n ->
    forall (M : Type u) [TopologicalSpace M] [T2Space M]
      [ChartedSpace (EuclideanModel n) M]
      [IsManifold (𝓡 n) ∞ M]
      [CompactSpace M],
        M ≃ₕ UnitSphere n -> Nonempty (M ≃ₜ UnitSphere n)

/-- Checked exhaustive recomposition of the two frozen dimension branches. -/
theorem highDimensionalPoincare_of_dimension_packages
    (dimensionFive : DimensionFivePackage.{u})
    (stable : StableDimensionPackage.{u}) :
    HighDimensionalPoincareTarget.{u} := by
  intro n hn M _ _ _ _ _ e
  by_cases hstable : 6 <= n
  · exact stable n hstable M e
  · have hn5 : n = 5 := by omega
    subst n
    exact dimensionFive M e

#print axioms highDimensionalPoincare_of_dimension_packages

end Stage1Instances.THMM0586
