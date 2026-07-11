import Mathlib.Geometry.Manifold.PoincareConjecture

/-!
# THM-M-0580: Perelman's theorem statement

This file freezes mathlib's topological three-dimensional Poincare-conjecture
formulation. It states the target and checks encodings around it; it does not
prove the conjecture.
-/

noncomputable section

open Metric (sphere)

namespace Stage1Instances.THM_M_0580

universe u

/-- Mathlib's Euclidean model for a topological three-manifold. -/
abbrev Euclidean3 := EuclideanSpace ℝ (Fin 3)

/-- The unit three-sphere in four-dimensional Euclidean space. -/
abbrev Sphere3 := sphere (0 : EuclideanSpace ℝ (Fin 4)) 1

/--
The exact topological three-dimensional Poincare target attributed to
Perelman: every compact Hausdorff simply connected topological
three-manifold is homeomorphic to the three-sphere.
-/
def PerelmanPoincareTarget : Prop :=
  ∀ (M : Type u) [TopologicalSpace M] [T2Space M]
    [ChartedSpace Euclidean3 M] [SimplyConnectedSpace M] [CompactSpace M],
    Nonempty (M ≃ₜ Sphere3)

/-- Direct expansion used to check that the local aliases hide no change. -/
def ExpandedTarget : Prop :=
  ∀ (M : Type u) [TopologicalSpace M] [T2Space M]
    [ChartedSpace (EuclideanSpace ℝ (Fin 3)) M]
    [SimplyConnectedSpace M] [CompactSpace M],
    Nonempty
      (M ≃ₜ sphere (0 : EuclideanSpace ℝ (Fin (3 + 1))) 1)

/-- The aliased target is definitionally identical to its direct expansion. -/
theorem perelmanPoincareTarget_iff_expandedTarget :
    PerelmanPoincareTarget.{u} ↔ ExpandedTarget.{u} := by
  rfl

-- Separately elaborated mutations, compared by `check_statement.py`.
def mutationRemovedT2 : Prop :=
  ∀ (M : Type u) [TopologicalSpace M]
    [ChartedSpace Euclidean3 M] [SimplyConnectedSpace M] [CompactSpace M],
    Nonempty (M ≃ₜ Sphere3)

def mutationRemovedCompact : Prop :=
  ∀ (M : Type u) [TopologicalSpace M] [T2Space M]
    [ChartedSpace Euclidean3 M] [SimplyConnectedSpace M],
    Nonempty (M ≃ₜ Sphere3)

def mutationChangedDimension : Prop :=
  ∀ (M : Type u) [TopologicalSpace M] [T2Space M]
    [ChartedSpace (EuclideanSpace ℝ (Fin 4)) M]
    [SimplyConnectedSpace M] [CompactSpace M],
    Nonempty
      (M ≃ₜ sphere (0 : EuclideanSpace ℝ (Fin 5)) 1)

def mutationConclusionOnlyNonempty : Prop :=
  ∀ (M : Type u) [TopologicalSpace M] [T2Space M]
    [ChartedSpace Euclidean3 M] [SimplyConnectedSpace M] [CompactSpace M],
    Nonempty M

end Stage1Instances.THM_M_0580

set_option pp.explicit true in
#print Stage1Instances.THM_M_0580.PerelmanPoincareTarget
