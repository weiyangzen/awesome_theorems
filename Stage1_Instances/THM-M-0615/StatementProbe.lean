import Mathlib.AlgebraicTopology.FundamentalGroupoid.SimplyConnected
import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Geometry.Manifold.IsManifold.Basic

/-!
# THM-M-0615 statement-surface probe

This module checks only the part of a simply connected closed topological
four-manifold classification statement that the pinned mathlib snapshot can
express without inventing invariant APIs. It is not the canonical target and
contains no classification theorem or proof.
-/

noncomputable section

open scoped Manifold

universe u v

namespace Stage1Instances.THM_M_0615

/-- The model space used to ask for a topological four-manifold as a `C^0`
manifold in the available mathlib API. -/
abbrev Euclidean4 : Type := EuclideanSpace ℝ (Fin 4)

/-- The boundaryless model with corners on four-dimensional Euclidean space. -/
abbrev TopologicalModel4 : ModelWithCorners ℝ Euclidean4 Euclidean4 :=
  𝓘(ℝ, Euclidean4)

/-- The source-side manifold assumptions which have direct pinned APIs.

`CompactSpace` supplies closedness because the selected model has no boundary;
the remaining typeclasses state Hausdorffness, connectedness, simple
connectedness, and the local four-dimensional `C^0` manifold condition.
-/
def AvailableSourceSideConditions
    (M : Type u) [TopologicalSpace M] [ChartedSpace Euclidean4 M]
    [T2Space M] [CompactSpace M] [ConnectedSpace M]
    [SimplyConnectedSpace M] [IsManifold TopologicalModel4 0 M] : Prop :=
  True

/-- The intended classification conclusion has a direct mathlib encoding. -/
def HomeomorphismConclusion
    (M : Type u) (N : Type v) [TopologicalSpace M] [TopologicalSpace N] : Prop :=
  Nonempty (M ≃ₜ N)

-- Pin the inferred types of the two available statement fragments.
set_option pp.explicit true in
#check AvailableSourceSideConditions

set_option pp.explicit true in
#check HomeomorphismConclusion

end Stage1Instances.THM_M_0615
