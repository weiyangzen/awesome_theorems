import Mathlib.Geometry.Manifold.Riemannian.Basic

/-!
# THM-M-0166: Hopf-Rinow statement

This module freezes the forward, minimizing-geodesic form of Hopf-Rinow. It
defines a proposition only; it does not assert or prove that proposition.
-/

noncomputable section

open Bundle Set Manifold
open scoped Bundle ContDiff ENNReal Manifold

namespace Stage1Instances.THM_M_0166

universe uE uH uM

/-- A path on `[0, 1]` is a minimizing geodesic segment when every ordered
subsegment realizes the Riemannian extended distance between its endpoints.
This metric characterization avoids selecting a connection convention. -/
def IsMinimizingGeodesicSegment
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {H : Type uH} [TopologicalSpace H] {I : ModelWithCorners ℝ E H}
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M]
    [∀ x : M, ENorm (TangentSpace I x)]
    (γ : ℝ → M) : Prop :=
  CMDiff[Icc (0 : ℝ) 1] ∞ γ ∧
    ∀ ⦃a b : ℝ⦄, a ∈ Icc (0 : ℝ) 1 → b ∈ Icc (0 : ℝ) 1 → a ≤ b →
      pathELength I γ a b = riemannianEDist I (γ a) (γ b)

/-- The exact forward Hopf-Rinow target: a connected, finite-dimensional,
boundaryless smooth Riemannian manifold that is complete for its Riemannian
metric admits a length-minimizing geodesic segment between every two points. -/
def HopfRinowStatement : Prop :=
  ∀ (E : Type uE) [NormedAddCommGroup E] [NormedSpace ℝ E] [FiniteDimensional ℝ E]
    (H : Type uH) [TopologicalSpace H] (I : ModelWithCorners ℝ E H)
    (M : Type uM) [EMetricSpace M] [ChartedSpace H M]
    [IsManifold I ∞ M] [BoundarylessManifold I M]
    [RiemannianBundle (fun x : M ↦ TangentSpace I x)]
    [IsContMDiffRiemannianBundle I ∞ E (fun x : M ↦ TangentSpace I x)]
    [IsRiemannianManifold I M] [ConnectedSpace M] [CompleteSpace M],
    ∀ p q : M, ∃ γ : ℝ → M,
      γ 0 = p ∧ γ 1 = q ∧ IsMinimizingGeodesicSegment (I := I) γ

-- Structural mutations elaborated independently by `check_statement.py`.
def MutationRemovedCompleteness : Prop :=
  ∀ (E : Type uE) [NormedAddCommGroup E] [NormedSpace ℝ E] [FiniteDimensional ℝ E]
    (H : Type uH) [TopologicalSpace H] (I : ModelWithCorners ℝ E H)
    (M : Type uM) [EMetricSpace M] [ChartedSpace H M]
    [IsManifold I ∞ M] [BoundarylessManifold I M]
    [RiemannianBundle (fun x : M ↦ TangentSpace I x)]
    [IsContMDiffRiemannianBundle I ∞ E (fun x : M ↦ TangentSpace I x)]
    [IsRiemannianManifold I M] [ConnectedSpace M],
    ∀ p q : M, ∃ γ : ℝ → M,
      γ 0 = p ∧ γ 1 = q ∧ IsMinimizingGeodesicSegment (I := I) γ

def MutationRemovedConnectedness : Prop :=
  ∀ (E : Type uE) [NormedAddCommGroup E] [NormedSpace ℝ E] [FiniteDimensional ℝ E]
    (H : Type uH) [TopologicalSpace H] (I : ModelWithCorners ℝ E H)
    (M : Type uM) [EMetricSpace M] [ChartedSpace H M]
    [IsManifold I ∞ M] [BoundarylessManifold I M]
    [RiemannianBundle (fun x : M ↦ TangentSpace I x)]
    [IsContMDiffRiemannianBundle I ∞ E (fun x : M ↦ TangentSpace I x)]
    [IsRiemannianManifold I M] [CompleteSpace M],
    ∀ p q : M, ∃ γ : ℝ → M,
      γ 0 = p ∧ γ 1 = q ∧ IsMinimizingGeodesicSegment (I := I) γ

def MutationArbitrarySmoothPath : Prop :=
  ∀ (E : Type uE) [NormedAddCommGroup E] [NormedSpace ℝ E] [FiniteDimensional ℝ E]
    (H : Type uH) [TopologicalSpace H] (I : ModelWithCorners ℝ E H)
    (M : Type uM) [EMetricSpace M] [ChartedSpace H M]
    [IsManifold I ∞ M] [BoundarylessManifold I M]
    [RiemannianBundle (fun x : M ↦ TangentSpace I x)]
    [IsContMDiffRiemannianBundle I ∞ E (fun x : M ↦ TangentSpace I x)]
    [IsRiemannianManifold I M] [ConnectedSpace M] [CompleteSpace M],
    ∀ p q : M, ∃ γ : ℝ → M,
      γ 0 = p ∧ γ 1 = q ∧ CMDiff[Icc (0 : ℝ) 1] ∞ γ

def MutationChangedEndpointScope : Prop :=
  ∀ (E : Type uE) [NormedAddCommGroup E] [NormedSpace ℝ E] [FiniteDimensional ℝ E]
    (H : Type uH) [TopologicalSpace H] (I : ModelWithCorners ℝ E H)
    (M : Type uM) [EMetricSpace M] [ChartedSpace H M]
    [IsManifold I ∞ M] [BoundarylessManifold I M]
    [RiemannianBundle (fun x : M ↦ TangentSpace I x)]
    [IsContMDiffRiemannianBundle I ∞ E (fun x : M ↦ TangentSpace I x)]
    [IsRiemannianManifold I M] [ConnectedSpace M] [CompleteSpace M],
    ∃ γ : ℝ → M, ∀ p q : M,
      γ 0 = p ∧ γ 1 = q ∧ IsMinimizingGeodesicSegment (I := I) γ

#check HopfRinowStatement
set_option pp.universes true in
#print HopfRinowStatement

end Stage1Instances.THM_M_0166
