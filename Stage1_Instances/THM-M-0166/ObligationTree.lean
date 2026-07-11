import Mathlib.Geometry.Manifold.Riemannian.Basic

/-!
# THM-M-0166 obligation composition harness

This file re-elaborates the frozen target and checks the two top-level
composition edges. It supplies no Hopf-Rinow proof body: both mathematical
packages are explicit hypotheses of the composition declarations.
-/

noncomputable section

open Bundle Set Manifold
open scoped Bundle ContDiff ENNReal Manifold

namespace Stage1Instances.THM_M_0166_Obligations

universe uE uH uM

def IsMinimizingGeodesicSegment
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {H : Type uH} [TopologicalSpace H] {I : ModelWithCorners ℝ E H}
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M]
    [∀ x : M, ENorm (TangentSpace I x)]
    (γ : ℝ → M) : Prop :=
  CMDiff[Icc (0 : ℝ) 1] ∞ γ ∧
    ∀ ⦃a b : ℝ⦄, a ∈ Icc (0 : ℝ) 1 → b ∈ Icc (0 : ℝ) 1 → a ≤ b →
      pathELength I γ a b = riemannianEDist I (γ a) (γ b)

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

/-- Open package: completeness supplies enough compactness to extract a
smooth path attaining the endpoint distance. -/
def GlobalMinimizerExistence : Prop :=
  ∀ (E : Type uE) [NormedAddCommGroup E] [NormedSpace ℝ E] [FiniteDimensional ℝ E]
    (H : Type uH) [TopologicalSpace H] (I : ModelWithCorners ℝ E H)
    (M : Type uM) [EMetricSpace M] [ChartedSpace H M]
    [IsManifold I ∞ M] [BoundarylessManifold I M]
    [RiemannianBundle (fun x : M ↦ TangentSpace I x)]
    [IsContMDiffRiemannianBundle I ∞ E (fun x : M ↦ TangentSpace I x)]
    [IsRiemannianManifold I M] [ConnectedSpace M] [CompleteSpace M],
    ∀ p q : M, ∃ γ : ℝ → M,
      γ 0 = p ∧ γ 1 = q ∧ CMDiff[Icc (0 : ℝ) 1] ∞ γ ∧
        pathELength I γ 0 1 = riemannianEDist I p q

/-- Open package: a smooth endpoint minimizer minimizes every ordered
subsegment. Its eventual proof must expose path restriction/concatenation and
length additivity rather than treating this implication as automatic. -/
def SubsegmentMinimality : Prop :=
  ∀ (E : Type uE) [NormedAddCommGroup E] [NormedSpace ℝ E]
    (H : Type uH) [TopologicalSpace H] (I : ModelWithCorners ℝ E H)
    (M : Type uM) [EMetricSpace M] [ChartedSpace H M]
    [RiemannianBundle (fun x : M ↦ TangentSpace I x)] [IsRiemannianManifold I M]
    (γ : ℝ → M),
    CMDiff[Icc (0 : ℝ) 1] ∞ γ →
    pathELength I γ 0 1 = riemannianEDist I (γ 0) (γ 1) →
    ∀ ⦃a b : ℝ⦄, a ∈ Icc (0 : ℝ) 1 → b ∈ Icc (0 : ℝ) 1 → a ≤ b →
      pathELength I γ a b = riemannianEDist I (γ a) (γ b)

/-- Checked child-to-parent composition. This theorem deliberately consumes
both open packages and introduces no theorem-specific premise. -/
theorem compose_root
    (existence : GlobalMinimizerExistence.{uE, uH, uM})
    (subsegments : SubsegmentMinimality.{uE, uH, uM}) :
    HopfRinowStatement.{uE, uH, uM} := by
  intro E _ _ _ H _ I M _ _ _ _ _ _ _ _ _ p q
  obtain ⟨γ, h0, h1, hsmooth, hmin⟩ := existence E H I M p q
  refine ⟨γ, h0, h1, hsmooth, ?_⟩
  exact subsegments E H I M γ hsmooth (h0 ▸ h1 ▸ hmin)

#check compose_root
set_option pp.universes true in
#print HopfRinowStatement
#print axioms compose_root

end Stage1Instances.THM_M_0166_Obligations
