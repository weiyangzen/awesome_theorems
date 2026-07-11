import Mathlib.Geometry.Manifold.PoincareConjecture

/-!
# THM-M-0579: exact statement boundary

This module elaborates the topological three-dimensional Poincare theorem using
the same object model as the pinned mathlib statement module. It names a
proposition only and makes no proof claim.
-/

noncomputable section

universe u

namespace Stage1Instances.THMM0579

/-- Euclidean three-space, used as the local model for the manifold charts. -/
abbrev ModelSpace3 : Type :=
  EuclideanSpace ℝ (Fin 3)

/-- The unit three-sphere in Euclidean four-space. -/
abbrev Sphere3 : Type :=
  Metric.sphere (0 : EuclideanSpace ℝ (Fin 4)) (1 : ℝ)

/--
Every compact Hausdorff simply connected topological three-manifold without
boundary is homeomorphic to the three-sphere.

`ChartedSpace ModelSpace3 M` expresses a boundaryless topological manifold
modeled on Euclidean three-space. `SimplyConnectedSpace M` includes the
connectedness required by the human statement.
-/
def Statement : Prop :=
  ∀ (M : Type u) [TopologicalSpace M] [T2Space M]
    [ChartedSpace ModelSpace3 M] [SimplyConnectedSpace M] [CompactSpace M],
    Nonempty (M ≃ₜ Sphere3)

/-- A named-hypothesis encoding used only as a checked alternate presentation. -/
def ClosedSimplyConnectedThreeManifold
    (M : Type u) [TopologicalSpace M] : Prop :=
  Nonempty (T2Space M) ∧
    Nonempty (ChartedSpace ModelSpace3 M) ∧
    Nonempty (SimplyConnectedSpace M) ∧
    Nonempty (CompactSpace M)

/-- Alternate predicate-style presentation of the same statement. -/
def NamedStatement : Prop :=
  ∀ (M : Type u) [TopologicalSpace M],
    ClosedSimplyConnectedThreeManifold M → Nonempty (M ≃ₜ Sphere3)

/-- Checked transport between the direct and named-hypothesis encodings. -/
theorem namedStatement_iff_statement : NamedStatement.{u} ↔ Statement.{u} := by
  constructor
  · intro h M _ _ _ _ _
    exact h M ⟨⟨inferInstance⟩, ⟨inferInstance⟩, ⟨inferInstance⟩, ⟨inferInstance⟩⟩
  · intro h M _ hM
    rcases hM with ⟨hT2, hCharted, hSimplyConnected, hCompact⟩
    letI : T2Space M := hT2.some
    letI : ChartedSpace ModelSpace3 M := hCharted.some
    letI : SimplyConnectedSpace M := hSimplyConnected.some
    letI : CompactSpace M := hCompact.some
    exact h M

#check Statement
#check namedStatement_iff_statement

end Stage1Instances.THMM0579
