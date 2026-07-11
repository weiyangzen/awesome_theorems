import Mathlib.Geometry.Manifold.PoincareConjecture

/-!
# THM-M-0583: four-dimensional topological Poincare theorem

This module specializes mathlib's object model for the generalized topological
Poincare conjecture to dimension four. It states the target only and does not
use the proof-wanted declaration in the imported module.
-/

noncomputable section

open Metric ContinuousMap
open scoped Manifold

namespace Stage1Instances.THM_M_0583

universe u

/-- The Euclidean model space for a topological four-manifold. -/
abbrev FourModel := EuclideanSpace ℝ (Fin 4)

/-- The standard topological four-sphere in five-dimensional Euclidean space. -/
abbrev FourSphere :=
  sphere (0 : EuclideanSpace ℝ (Fin 5)) 1

/-- Every topological four-manifold homotopy equivalent to the standard
four-sphere is homeomorphic to it. The `ChartedSpace` and `T2Space` instances
are mathlib's boundaryless topological-manifold convention for this target. -/
def FourDimensionalTopologicalPoincareTarget : Prop :=
  ∀ (M : Type u) [TopologicalSpace M] [T2Space M] [CompactSpace M]
    [ChartedSpace FourModel M],
    M ≃ₕ FourSphere → Nonempty (M ≃ₜ FourSphere)

/-- Checked expansion fixing all binders, the dimension, and the conclusion. -/
theorem fourDimensionalTopologicalPoincareTarget_iff_expanded :
    FourDimensionalTopologicalPoincareTarget.{u} ↔
      ∀ (M : Type u) [TopologicalSpace M] [T2Space M]
        [CompactSpace M] [ChartedSpace (EuclideanSpace ℝ (Fin 4)) M],
          M ≃ₕ sphere (0 : EuclideanSpace ℝ (Fin 5)) 1 →
            Nonempty (M ≃ₜ sphere (0 : EuclideanSpace ℝ (Fin 5)) 1) :=
  Iff.rfl

-- Structural mutations are elaborated separately and receive no equivalence credit.
def mutationRemovedHomotopyEquivalence : Prop :=
  ∀ (M : Type u) [TopologicalSpace M] [T2Space M] [CompactSpace M]
    [ChartedSpace FourModel M],
    Nonempty (M ≃ₜ FourSphere)

def mutationChangedDimension : Prop :=
  ∀ (M : Type u) [TopologicalSpace M] [T2Space M]
    [CompactSpace M] [ChartedSpace (EuclideanSpace ℝ (Fin 3)) M],
      M ≃ₕ sphere (0 : EuclideanSpace ℝ (Fin 4)) 1 →
        Nonempty (M ≃ₜ sphere (0 : EuclideanSpace ℝ (Fin 4)) 1)

def mutationChangedBinderScope : Prop :=
  ∃ (M : Type u) (_ : TopologicalSpace M) (_ : T2Space M)
    (_ : CompactSpace M) (_ : ChartedSpace FourModel M),
      M ≃ₕ FourSphere → Nonempty (M ≃ₜ FourSphere)

def mutationRemovedCompactness : Prop :=
  ∀ (M : Type u) [TopologicalSpace M] [T2Space M] [ChartedSpace FourModel M],
    M ≃ₕ FourSphere → Nonempty (M ≃ₜ FourSphere)

end Stage1Instances.THM_M_0583

set_option pp.universes true in
set_option pp.explicit true in
#print Stage1Instances.THM_M_0583.FourDimensionalTopologicalPoincareTarget
