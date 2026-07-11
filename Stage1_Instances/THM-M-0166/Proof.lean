import Mathlib.Geometry.Manifold.Riemannian.Basic

/-!
# THM-M-0166 proof bodies

This module closes the subsegment-minimality child of the frozen Hopf-Rinow
architecture.  The global-minimizer existence child remains outside the
current pinned mathlib surface.
-/

noncomputable section

open Bundle Set Manifold
open scoped Bundle ContDiff ENNReal Manifold

namespace Stage1Instances.THM_M_0166_Proof

universe uE uH uM

/-- In a connected extended metric space every pair of points has finite
extended distance. -/
lemma edist_ne_top_of_connected
    {M : Type uM} [EMetricSpace M] [ConnectedSpace M] (p q : M) :
    edist p q ≠ (∞ : ℝ≥0∞) := by
  have hclopen : IsClopen (Metric.eball p (∞ : ℝ≥0∞)) :=
    ⟨Metric.isClosed_eball_top, Metric.isOpen_eball⟩
  have huniv : (Set.univ : Set M) ⊆ Metric.eball p (∞ : ℝ≥0∞) :=
    isPreconnected_univ.subset_isClopen hclopen
      ⟨p, Set.mem_univ p, Metric.mem_eball_self ENNReal.coe_lt_top⟩
  have hqp : edist q p < (∞ : ℝ≥0∞) := huniv (Set.mem_univ q)
  rw [edist_comm] at hqp
  exact ne_of_lt hqp

/-- A globally minimizing smooth path minimizes each ordered subsegment.

The proof uses only distance triangle inequalities, lower bounds of distance
by path length, path-length additivity, and cancellation justified by the
finiteness supplied by connectedness. -/
theorem subsegmentMinimality
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {H : Type uH} [TopologicalSpace H] (I : ModelWithCorners ℝ E H)
    {M : Type uM} [EMetricSpace M] [ChartedSpace H M]
    [RiemannianBundle (fun x : M ↦ TangentSpace I x)] [IsRiemannianManifold I M]
    [ConnectedSpace M]
    (γ : ℝ → M)
    (hsmooth : CMDiff[Icc (0 : ℝ) 1] ∞ γ)
    (hmin : pathELength I γ 0 1 = riemannianEDist I (γ 0) (γ 1)) :
    ∀ ⦃a b : ℝ⦄, a ∈ Icc (0 : ℝ) 1 → b ∈ Icc (0 : ℝ) 1 → a ≤ b →
      pathELength I γ a b = riemannianEDist I (γ a) (γ b) := by
  intro a b ha hb hab
  have hsmooth' : CMDiff[Icc (0 : ℝ) 1] 1 γ := hsmooth.of_le (by simp)
  have h0a : riemannianEDist I (γ 0) (γ a) ≤ pathELength I γ 0 a := by
    apply riemannianEDist_le_pathELength
    · exact hsmooth'.mono (Icc_subset_Icc le_rfl ha.2)
    · rfl
    · rfl
    · exact ha.1
  have hab' : riemannianEDist I (γ a) (γ b) ≤ pathELength I γ a b := by
    apply riemannianEDist_le_pathELength
    · exact hsmooth'.mono (Icc_subset_Icc ha.1 hb.2)
    · rfl
    · rfl
    · exact hab
  have hb1 : riemannianEDist I (γ b) (γ 1) ≤ pathELength I γ b 1 := by
    apply riemannianEDist_le_pathELength
    · exact hsmooth'.mono (Icc_subset_Icc hb.1 le_rfl)
    · rfl
    · rfl
    · exact hb.2
  have htriangle :
      riemannianEDist I (γ 0) (γ 1) ≤
        riemannianEDist I (γ 0) (γ a) + riemannianEDist I (γ a) (γ b) +
          riemannianEDist I (γ b) (γ 1) := by
    calc
      _ ≤ riemannianEDist I (γ 0) (γ a) + riemannianEDist I (γ a) (γ 1) :=
        riemannianEDist_triangle
      _ ≤ _ := by
        rw [add_assoc]
        exact add_le_add le_rfl
          (riemannianEDist_triangle (I := I) (x := γ a) (y := γ b) (z := γ 1))
  have hchain :
      pathELength I γ 0 1 ≤
        pathELength I γ 0 a + riemannianEDist I (γ a) (γ b) +
          pathELength I γ b 1 := by
    rw [hmin]
    exact htriangle.trans (add_le_add (add_le_add h0a le_rfl) hb1)
  have htotal :
      pathELength I γ 0 a + pathELength I γ a b + pathELength I γ b 1 =
        pathELength I γ 0 1 := by
    rw [pathELength_add ha.1 hab]
    exact pathELength_add (I := I) (γ := γ) (a := 0) (b := b) (c := 1)
      (ha.1.trans hab) hb.2
  have hreverse :
      pathELength I γ 0 a + riemannianEDist I (γ a) (γ b) +
          pathELength I γ b 1 ≤ pathELength I γ 0 1 := by
    rw [← htotal]
    gcongr
  have heq :
      pathELength I γ 0 a + riemannianEDist I (γ a) (γ b) +
          pathELength I γ b 1 =
        pathELength I γ 0 a + pathELength I γ a b + pathELength I γ b 1 := by
    rw [htotal]
    exact le_antisymm hreverse hchain
  have htotal_ne : pathELength I γ 0 1 ≠ (∞ : ℝ≥0∞) := by
    rw [hmin, ← IsRiemannianManifold.out]
    exact edist_ne_top_of_connected (γ 0) (γ 1)
  have hleft_ne : pathELength I γ 0 a ≠ (∞ : ℝ≥0∞) := by
    exact ne_top_of_le_ne_top htotal_ne (pathELength_mono le_rfl ha.2)
  have hright_ne : pathELength I γ b 1 ≠ (∞ : ℝ≥0∞) := by
    exact ne_top_of_le_ne_top htotal_ne (pathELength_mono hb.1 le_rfl)
  apply (add_right_injective_of_ne_top _ hright_ne)
  apply (add_right_injective_of_ne_top _ hleft_ne)
  simpa [add_assoc, add_comm, add_left_comm] using heq.symm

/-- Checked direct composition from the remaining global-minimizer package to
the exact all-subsegments conclusion. -/
theorem hopfRinow_of_globalMinimizers
    (existence :
      ∀ (E : Type uE) [NormedAddCommGroup E] [NormedSpace ℝ E]
        [FiniteDimensional ℝ E]
        (H : Type uH) [TopologicalSpace H] (I : ModelWithCorners ℝ E H)
        (M : Type uM) [EMetricSpace M] [ChartedSpace H M]
        [IsManifold I ∞ M] [BoundarylessManifold I M]
        [RiemannianBundle (fun x : M ↦ TangentSpace I x)]
        [IsContMDiffRiemannianBundle I ∞ E (fun x : M ↦ TangentSpace I x)]
        [IsRiemannianManifold I M] [ConnectedSpace M] [CompleteSpace M],
        ∀ p q : M, ∃ γ : ℝ → M,
          γ 0 = p ∧ γ 1 = q ∧ CMDiff[Icc (0 : ℝ) 1] ∞ γ ∧
            pathELength I γ 0 1 = riemannianEDist I p q) :
    ∀ (E : Type uE) [NormedAddCommGroup E] [NormedSpace ℝ E]
      [FiniteDimensional ℝ E]
      (H : Type uH) [TopologicalSpace H] (I : ModelWithCorners ℝ E H)
      (M : Type uM) [EMetricSpace M] [ChartedSpace H M]
      [IsManifold I ∞ M] [BoundarylessManifold I M]
      [RiemannianBundle (fun x : M ↦ TangentSpace I x)]
      [IsContMDiffRiemannianBundle I ∞ E (fun x : M ↦ TangentSpace I x)]
      [IsRiemannianManifold I M] [ConnectedSpace M] [CompleteSpace M],
      ∀ p q : M, ∃ γ : ℝ → M,
        γ 0 = p ∧ γ 1 = q ∧
          (CMDiff[Icc (0 : ℝ) 1] ∞ γ ∧
            ∀ ⦃a b : ℝ⦄, a ∈ Icc (0 : ℝ) 1 → b ∈ Icc (0 : ℝ) 1 → a ≤ b →
              pathELength I γ a b = riemannianEDist I (γ a) (γ b)) := by
  intro E _ _ _ H _ I M _ _ _ _ _ _ _ _ _ p q
  obtain ⟨γ, h0, h1, hsmooth, hmin⟩ := existence E H I M p q
  refine ⟨γ, h0, h1, hsmooth, ?_⟩
  apply subsegmentMinimality I γ hsmooth
  simpa [h0, h1] using hmin

#print axioms subsegmentMinimality
#print axioms hopfRinow_of_globalMinimizers

end Stage1Instances.THM_M_0166_Proof
