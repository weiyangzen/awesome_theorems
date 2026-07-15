import «Stage1_Instances».«THM-M-0321».ObligationTree
import Mathlib.Analysis.Convex.Combination
import Mathlib.Analysis.LocallyConvex.Bounded
import Mathlib.Analysis.SpecificLimits.Basic
import Mathlib.Topology.Ultrafilter

/-!
# THM-M-0321 proof bodies

This module implements the one-map averaging argument, finite-family
induction, and compact finite-intersection part of the Markov-Kakutani proof.
-/

open Filter Function Set Topology

namespace Stage1Instances.THM_M_0321

universe u v

/-- Points of `K` fixed by `g`. -/
def fixedSetWithin {E : Type u} (K : Set E) (g : E → E) : Set E :=
  {x | x ∈ K ∧ g x = x}

theorem isClosed_fixedSetWithin {E : Type u} [TopologicalSpace E] [T2Space E]
    {K : Set E} {g : E → E} (hK : IsClosed K) (hg : ContinuousOn g K) :
    IsClosed (fixedSetWithin K g) := by
  simpa [fixedSetWithin] using hK.isClosed_eq hg continuousOn_id

theorem isCompact_fixedSetWithin {E : Type u} [TopologicalSpace E] [T2Space E]
    {K : Set E} {g : E → E} (hK : IsCompact K) (hg : ContinuousOn g K) :
    IsCompact (fixedSetWithin K g) := by
  exact IsCompact.of_isClosed_subset hK
    (isClosed_fixedSetWithin hK.isClosed hg) (fun _ hx ↦ hx.1)

theorem convex_fixedSetWithin {E : Type u} [AddCommGroup E] [Module ℝ E]
    {K : Set E} {g : E → E} (hK : Convex ℝ K) (hg : IsAffineOn K g) :
    Convex ℝ (fixedSetWithin K g) := by
  rw [convex_iff_segment_subset]
  intro x hx y hy z hz
  obtain ⟨a, b, ha, hb, hab, rfl⟩ := hz
  have hcombo : a • x + b • y ∈ K := hK hx.1 hy.1 ha hb hab
  refine ⟨hcombo, ?_⟩
  rw [hg x hx.1 y hy.1 a b ha hb hab, hx.2, hy.2]

theorem mapsTo_fixedSetWithin_of_commute {E : Type u}
    {K : Set E} {g h : E → E} (hh : MapsTo h K K)
    (hcomm : ∀ x ∈ K, g (h x) = h (g x)) :
    MapsTo h (fixedSetWithin K g) (fixedSetWithin K g) := by
  rintro x ⟨hxK, hxg⟩
  refine ⟨hh hxK, ?_⟩
  rw [hcomm x hxK, hxg]

theorem continuousOn_fixedSetWithin {E : Type u} [TopologicalSpace E]
    {K : Set E} {g h : E → E} (hh : ContinuousOn h K) :
    ContinuousOn h (fixedSetWithin K g) :=
  hh.mono fun _ hx ↦ hx.1

theorem isAffineOn_fixedSetWithin {E : Type u} [AddCommGroup E] [Module ℝ E]
    {K : Set E} {g h : E → E} (hh : IsAffineOn K h) :
    IsAffineOn (fixedSetWithin K g) h := by
  intro x hx y hy a b ha hb hab
  exact hh x hx.1 y hy.1 a b ha hb hab

/-- The Cesaro average of the first `n + 1` iterates of `x` under `g`. -/
noncomputable def cesaroAverage {E : Type u} [AddCommGroup E] [Module ℝ E]
    (g : E → E) (x : E) (n : ℕ) : E :=
  ((n + 1 : ℕ) : ℝ)⁻¹ • ∑ k ∈ Finset.range (n + 1), (g^[k]) x

theorem iterate_mem {E : Type u} {K : Set E} {g : E → E}
    (hg : MapsTo g K K) {x : E} (hx : x ∈ K) (n : ℕ) : (g^[n]) x ∈ K := by
  induction n with
  | zero => simpa
  | succ n hn => simpa [Function.iterate_succ_apply'] using hg hn

theorem cesaroAverage_mem {E : Type u} [AddCommGroup E] [Module ℝ E]
    {K : Set E} {g : E → E} (hK : Convex ℝ K) (hg : MapsTo g K K)
    {x : E} (hx : x ∈ K) (n : ℕ) : cesaroAverage g x n ∈ K := by
  unfold cesaroAverage
  have heq :
      ((n + 1 : ℕ) : ℝ)⁻¹ • ∑ k ∈ Finset.range (n + 1), (g^[k]) x =
        (Finset.range (n + 1)).centerMass (fun _ ↦ (1 : ℝ)) (fun k ↦ (g^[k]) x) := by
    simp [Finset.centerMass]
  rw [heq]
  exact hK.centerMass_mem (fun _ _ ↦ by norm_num) (by
    simp only [Finset.sum_const, Finset.card_range, nsmul_eq_mul, mul_one]
    positivity) fun k _ ↦ iterate_mem hg hx k

theorem affine_centerMass {E : Type u} [AddCommGroup E] [Module ℝ E]
    {K : Set E} {g : E → E} (hg : IsAffineOn K g)
    (hK : Convex ℝ K) {t : Finset ℕ} {z : ℕ → E} (hz : ∀ i ∈ t, z i ∈ K)
    {w : ℕ → ℝ} (hw0 : ∀ i ∈ t, 0 ≤ w i) (hw : 0 < ∑ i ∈ t, w i) :
    g (t.centerMass w z) = t.centerMass w (g ∘ z) := by
  classical
  induction t using Finset.induction with
  | empty => simp at hw
  | @insert i t hi ih =>
      have hiK : z i ∈ K := hz i (Finset.mem_insert_self _ _)
      have htK : ∀ j ∈ t, z j ∈ K := fun j hj ↦ hz j (Finset.mem_insert_of_mem hj)
      have hiw : 0 ≤ w i := hw0 i (Finset.mem_insert_self _ _)
      have htw : ∀ j ∈ t, 0 ≤ w j := fun j hj ↦ hw0 j (Finset.mem_insert_of_mem hj)
      by_cases hsum : ∑ j ∈ t, w j = 0
      · have wz : ∀ j ∈ t, w j = 0 := (Finset.sum_eq_zero_iff_of_nonneg htw).1 hsum
        have hwi : w i ≠ 0 := by
          rw [Finset.sum_insert hi, hsum, add_zero] at hw
          exact ne_of_gt hw
        have hleft : (insert i t).centerMass w z = z i := by
          rw [Finset.centerMass]
          simp only [Finset.sum_insert hi, hsum, add_zero]
          have htz : ∑ j ∈ t, w j • z j = 0 := Finset.sum_eq_zero fun j hj ↦ by
            rw [wz j hj, zero_smul]
          rw [htz, add_zero]
          simp [hwi]
        have hright : (insert i t).centerMass w (g ∘ z) = g (z i) := by
          rw [Finset.centerMass]
          simp only [Finset.sum_insert hi, hsum, add_zero]
          have htgz : ∑ j ∈ t, w j • (g ∘ z) j = 0 := Finset.sum_eq_zero fun j hj ↦ by
            rw [wz j hj, zero_smul]
          rw [htgz, add_zero]
          simp [hwi]
        rw [hleft, hright]
      · rw [Finset.centerMass_insert _ _ _ hi hsum]
        rw [Finset.centerMass_insert _ _ _ hi hsum]
        have hsum_nonneg : 0 ≤ ∑ j ∈ t, w j := Finset.sum_nonneg htw
        have hsum_pos : 0 < ∑ j ∈ t, w j := lt_of_le_of_ne hsum_nonneg (Ne.symm hsum)
        have hden : 0 < w i + ∑ j ∈ t, w j := by
          rw [Finset.sum_insert hi] at hw
          exact hw
        have hcenter : t.centerMass w z ∈ K := hK.centerMass_mem htw hsum_pos htK
        rw [hg _ hiK _ hcenter _ _ (div_nonneg hiw hden.le) (div_nonneg hsum_nonneg hden.le)
          (by field_simp)]
        rw [ih htK htw hsum_pos]
        rfl

theorem map_cesaroAverage {E : Type u} [AddCommGroup E] [Module ℝ E]
    {K : Set E} {g : E → E} (hK : Convex ℝ K) (hgK : MapsTo g K K)
    (hg : IsAffineOn K g) {x : E} (hx : x ∈ K) (n : ℕ) :
    g (cesaroAverage g x n) =
      ((n + 1 : ℕ) : ℝ)⁻¹ • ∑ k ∈ Finset.range (n + 1), (g^[k + 1]) x := by
  unfold cesaroAverage
  have heq :
      ((n + 1 : ℕ) : ℝ)⁻¹ • ∑ k ∈ Finset.range (n + 1), (g^[k]) x =
        (Finset.range (n + 1)).centerMass (fun _ ↦ (1 : ℝ)) (fun k ↦ (g^[k]) x) := by
    simp [Finset.centerMass]
  rw [heq]
  rw [affine_centerMass hg hK (fun k _ ↦ iterate_mem hgK hx k)
    (fun _ _ ↦ by norm_num) (by
      simp only [Finset.sum_const, Finset.card_range, nsmul_eq_mul, mul_one]
      positivity)]
  simp only [Finset.centerMass, Finset.sum_const, Finset.card_range, nsmul_eq_mul, mul_one,
    Nat.cast_add, Nat.cast_one, comp_apply, Function.iterate_succ_apply']
  simp only [one_smul]

theorem cesaro_defect_eq {E : Type u} [AddCommGroup E] [Module ℝ E]
    {K : Set E} {g : E → E} (hK : Convex ℝ K) (hgK : MapsTo g K K)
    (hg : IsAffineOn K g) {x : E} (hx : x ∈ K) (n : ℕ) :
    g (cesaroAverage g x n) - cesaroAverage g x n =
      ((n + 1 : ℕ) : ℝ)⁻¹ • ((g^[n + 1]) x - x) := by
  rw [map_cesaroAverage hK hgK hg hx]
  unfold cesaroAverage
  rw [← smul_sub]
  congr 1
  rw [← Finset.sum_sub_distrib]
  have htel := Finset.sum_range_sub (fun k ↦ (g^[k]) x) (n + 1)
  simpa only [Function.iterate_zero_apply, Nat.add_comm] using htel

theorem tendsto_cesaro_defect_zero {E : Type u} [AddCommGroup E] [Module ℝ E]
    [TopologicalSpace E] [IsTopologicalAddGroup E] [ContinuousSMul ℝ E]
    {K : Set E} {g : E → E} (hK : Convex ℝ K) (hgK : MapsTo g K K)
    (hg : IsAffineOn K g) (hCompact : IsCompact K) {x : E} (hx : x ∈ K) :
    Tendsto (fun n ↦ g (cesaroAverage g x n) - cesaroAverage g x n) atTop (𝓝 0) := by
  letI := IsTopologicalAddGroup.rightUniformSpace E
  haveI := isUniformAddGroup_of_addCommGroup (G := E)
  have hBoundK : Bornology.IsVonNBounded ℝ K := hCompact.totallyBounded.isVonNBounded ℝ
  have hBound : Bornology.IsVonNBounded ℝ (K -ᵥ K) := hBoundK.sub hBoundK
  have hmem : ∀ n, (g^[n + 1]) x - x ∈ K -ᵥ K := fun n ↦
    Set.sub_mem_sub (iterate_mem hgK hx (n + 1)) hx
  have hscale : Tendsto (fun n : ℕ ↦ ((n + 1 : ℕ) : ℝ)⁻¹) atTop (𝓝 0) := by
    simpa only [one_div, Nat.cast_add, Nat.cast_one] using
      (tendsto_one_div_add_atTop_nhds_zero_nat (𝕜 := ℝ))
  have := hBound.smul_tendsto_zero (Eventually.of_forall hmem) hscale
  simpa only [Pi.smul_apply, cesaro_defect_eq hK hgK hg hx] using this

/-- A continuous affine self-map of a nonempty compact convex set has a fixed
point. The proof uses Cesaro averages of one orbit and compactness. -/
theorem singleMap_fixedPoint {E : Type u} [AddCommGroup E] [Module ℝ E]
    [TopologicalSpace E] [T2Space E] [IsTopologicalAddGroup E] [ContinuousSMul ℝ E]
    {K : Set E} {g : E → E} (hKne : K.Nonempty) (hCompact : IsCompact K)
    (hK : Convex ℝ K) (hgK : MapsTo g K K) (hgcont : ContinuousOn g K)
    (hg : IsAffineOn K g) : ∃ y ∈ K, g y = y := by
  obtain ⟨x, hx⟩ := hKne
  let A : ℕ → E := fun n ↦ cesaroAverage g x n
  have hAmem : ∀ n, A n ∈ K := fun n ↦ cesaroAverage_mem hK hgK hx n
  obtain ⟨y, hyK, hycluster⟩ := hCompact.exists_mapClusterPt
    (show Filter.map A atTop ≤ Filter.principal K by
      rw [Filter.le_principal_iff, Filter.mem_map]
      exact Filter.Eventually.of_forall (fun n : ℕ ↦ hAmem n))
  rw [mapClusterPt_iff_ultrafilter] at hycluster
  obtain ⟨U, hUtop, hUA⟩ := hycluster
  have hAKU : ∀ᶠ n in (U : Filter ℕ), A n ∈ K := Eventually.of_forall hAmem
  have hUAwithin : Tendsto A U (𝓝[K] y) :=
    tendsto_nhdsWithin_iff.mpr ⟨hUA, hAKU⟩
  have hUgA : Tendsto (fun n ↦ g (A n)) U (𝓝 (g y)) :=
    (hgcont y hyK).tendsto.comp hUAwithin
  have hUdefect : Tendsto (fun n ↦ g (A n) - A n) U (𝓝 0) :=
    (tendsto_cesaro_defect_zero hK hgK hg hCompact hx).mono_left hUtop
  have hUdefect' : Tendsto (fun n ↦ g (A n) - A n) U (𝓝 (g y - y)) := hUgA.sub hUA
  have : g y - y = 0 := tendsto_nhds_unique hUdefect' hUdefect
  exact ⟨y, hyK, sub_eq_zero.mp this⟩

/-- Points of `K` fixed by every member of the finite family `s`. -/
def commonFixedSet {E : Type u} {I : Type v}
    (K : Set E) (f : I → E → E) (s : Finset I) : Set E :=
  {x | x ∈ K ∧ ∀ i ∈ s, f i x = x}

theorem isClosed_commonFixedSet {E : Type u} {I : Type v}
    [TopologicalSpace E] [T2Space E] {K : Set E} {f : I → E → E}
    (hK : IsClosed K) (hcont : ∀ i, ContinuousOn (f i) K) (s : Finset I) :
    IsClosed (commonFixedSet K f s) := by
  rw [show commonFixedSet K f s = K ∩ ⋂ i ∈ s, fixedSetWithin K (f i) by
    ext x
    constructor
    · rintro ⟨hxK, hx⟩
      refine ⟨hxK, ?_⟩
      simp only [mem_iInter]
      exact fun i hi ↦ ⟨hxK, hx i hi⟩
    · rintro ⟨hxK, hx⟩
      refine ⟨hxK, fun i hi ↦ ?_⟩
      exact (mem_iInter.mp (mem_iInter.mp hx i) hi).2]
  exact hK.inter (isClosed_biInter fun i _ ↦ isClosed_fixedSetWithin hK (hcont i))

theorem isCompact_commonFixedSet {E : Type u} {I : Type v}
    [TopologicalSpace E] [T2Space E] {K : Set E} {f : I → E → E}
    (hK : IsCompact K) (hcont : ∀ i, ContinuousOn (f i) K) (s : Finset I) :
    IsCompact (commonFixedSet K f s) := by
  exact IsCompact.of_isClosed_subset hK
    (isClosed_commonFixedSet hK.isClosed hcont s) (fun _ hx ↦ hx.1)

theorem convex_commonFixedSet {E : Type u} {I : Type v}
    [AddCommGroup E] [Module ℝ E] {K : Set E} {f : I → E → E}
    (hK : Convex ℝ K) (haff : ∀ i, IsAffineOn K (f i)) (s : Finset I) :
    Convex ℝ (commonFixedSet K f s) := by
  rw [convex_iff_segment_subset]
  intro x hx y hy z hz
  obtain ⟨a, b, ha, hb, hab, rfl⟩ := hz
  have hcombo : a • x + b • y ∈ K := hK hx.1 hy.1 ha hb hab
  refine ⟨hcombo, fun i hi ↦ ?_⟩
  rw [haff i x hx.1 y hy.1 a b ha hb hab, hx.2 i hi, hy.2 i hi]

theorem mapsTo_commonFixedSet_of_commute {E : Type u} {I : Type v}
    {K : Set E} {f : I → E → E}
    (hmap : ∀ i, MapsTo (f i) K K)
    (hcomm : ∀ i j, ∀ x ∈ K, f i (f j x) = f j (f i x))
    (s : Finset I) (a : I) :
    MapsTo (f a) (commonFixedSet K f s) (commonFixedSet K f s) := by
  rintro x ⟨hxK, hx⟩
  refine ⟨hmap a hxK, fun i hi ↦ ?_⟩
  rw [hcomm i a x hxK, hx i hi]

/-- Every finite commuting subfamily has a common fixed point. The induction
applies the one-map theorem to the common fixed locus constructed so far. -/
theorem finiteFamilyStep : ObligationTree.FiniteFamilyStep.{u, v} := by
  intro E _ _ _ _ _ _ _ I K f hne hcompact hconvex hmap hcont haff hcomm s
  classical
  induction s using Finset.induction_on with
  | empty =>
      obtain ⟨x, hx⟩ := hne
      exact ⟨x, hx, by simp⟩
  | @insert a s ha ih =>
      let L := commonFixedSet K f s
      have hLne : L.Nonempty := by
        obtain ⟨x, hxK, hx⟩ := ih
        exact ⟨x, hxK, hx⟩
      have hLcompact : IsCompact L := isCompact_commonFixedSet hcompact hcont s
      have hLconvex : Convex ℝ L := convex_commonFixedSet hconvex haff s
      have hLmap : MapsTo (f a) L L := mapsTo_commonFixedSet_of_commute hmap hcomm s a
      have hLcont : ContinuousOn (f a) L := (hcont a).mono fun _ hx ↦ hx.1
      have hLaff : IsAffineOn L (f a) := by
        intro x hx y hy c d hc hd hcd
        exact haff a x hx.1 y hy.1 c d hc hd hcd
      obtain ⟨x, hxL, hxa⟩ := singleMap_fixedPoint
        hLne hLcompact hLconvex hLmap hLcont hLaff
      refine ⟨x, hxL.1, ?_⟩
      intro i hi
      rw [Finset.mem_insert] at hi
      rcases hi with rfl | hi
      · exact hxa
      · exact hxL.2 i hi

/-- The valid compact finite-intersection upgrade.  Unlike the provisional
frozen helper interface, this statement records the continuity needed to make
the fixed-point sets closed. -/
theorem continuousCompactnessUpgrade {E : Type u} [TopologicalSpace E] [T2Space E]
    {I : Type v} {K : Set E} {f : I → E → E}
    (hCompact : IsCompact K) (hContinuous : ∀ i, ContinuousOn (f i) K)
    (hFinite : ∀ s : Finset I, ∃ x ∈ K, ∀ i ∈ s, f i x = x) :
    HasCommonFixedPoint K f := by
  let F : I → Set E := fun i ↦ fixedSetWithin K (f i)
  have hClosed : ∀ i, IsClosed (F i) := fun i ↦
    isClosed_fixedSetWithin hCompact.isClosed (hContinuous i)
  have hFinite' : ∀ s : Finset I, (K ∩ ⋂ i ∈ s, F i).Nonempty := by
    intro s
    obtain ⟨x, hxK, hx⟩ := hFinite s
    refine ⟨x, hxK, ?_⟩
    simp only [mem_iInter]
    exact fun i hi ↦ ⟨hxK, hx i hi⟩
  obtain ⟨x, hxK, hx⟩ := hCompact.inter_iInter_nonempty F hClosed hFinite'
  refine ⟨x, hxK, fun i ↦ ?_⟩
  exact (mem_iInter.mp hx i).2

/-- Once finite subfamilies have common fixed points, the corrected compactness
upgrade closes the exact frozen root without any additional premise. -/
theorem markovKakutani_of_finiteFamily
    (finiteFamily : ObligationTree.FiniteFamilyStep.{u, v}) :
    MarkovKakutaniTarget.{u, v} := by
  intro E _ _ _ _ _ _ _ I K f hK hCompact hConvex hMaps hContinuous hAffine hCommute
  exact continuousCompactnessUpgrade hCompact hContinuous
    (finiteFamily E I K f hK hCompact hConvex hMaps hContinuous hAffine hCommute)

/-- The exact frozen Markov-Kakutani target. -/
theorem markovKakutani_proof : MarkovKakutaniTarget.{u, v} :=
  markovKakutani_of_finiteFamily finiteFamilyStep

#print axioms isClosed_fixedSetWithin
#print axioms isCompact_fixedSetWithin
#print axioms convex_fixedSetWithin
#print axioms mapsTo_fixedSetWithin_of_commute
#print axioms continuousOn_fixedSetWithin
#print axioms isAffineOn_fixedSetWithin
#print axioms cesaroAverage_mem
#print axioms affine_centerMass
#print axioms map_cesaroAverage
#print axioms cesaro_defect_eq
#print axioms tendsto_cesaro_defect_zero
#print axioms singleMap_fixedPoint
#print axioms isClosed_commonFixedSet
#print axioms isCompact_commonFixedSet
#print axioms convex_commonFixedSet
#print axioms mapsTo_commonFixedSet_of_commute
#print axioms finiteFamilyStep
#print axioms continuousCompactnessUpgrade
#print axioms markovKakutani_of_finiteFamily
#print axioms markovKakutani_proof

end Stage1Instances.THM_M_0321
