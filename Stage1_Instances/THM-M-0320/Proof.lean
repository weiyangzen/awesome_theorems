import ObligationTree
import GraphBridgeProof
import BrouwerSource
import Mathlib.Analysis.Convex.PartitionOfUnity
import Mathlib.Analysis.Normed.Module.Convex
import Mathlib.Analysis.Convex.Topology
import Mathlib.Topology.UniformSpace.HeineCantor
import Mathlib.Topology.MetricSpace.Pseudo.Basic
import Mathlib.Analysis.Convex.Caratheodory
import Mathlib.Util.AssertNoSorry

namespace Stage1Instances.THM_M_0320

open Filter Set

noncomputable section

open Classical

/-!
# THM-M-0320 proof

This file proves the frozen closed-graph Kakutani core by continuous convex
selection, a finite Caratheodory package, and compact sequential convergence.
Its only external mathematical terminal is the MIT-licensed simplex Brouwer
body recorded by `BrouwerSource.lean` and `brouwer-source.json`.
-/

/-- A fixed-length convex combination presentation. -/
def ConvexCombination {V : Type*} {k : Nat} [AddCommGroup V] [Module Real V]
    (x : V) (a : Fin k -> Real) (y : Fin k -> V) : Prop :=
  (forall i, 0 <= a i) /\ (∑ i, a i) = 1 /\ x = ∑ i, a i • y i

lemma mem_of_convexCombination {V : Type*} {k : Nat}
    [AddCommGroup V] [Module Real V]
    (x : V) {a : Fin k -> Real} {y : Fin k -> V}
    (h : ConvexCombination x a y) (s : Set V) (hs : Convex Real s)
    (hy : forall i, y i ∈ s) : x ∈ s := by
  rw [h.2.2]
  exact hs.sum_mem (fun i _ => h.1 i) h.2.1 (fun i _ => hy i)

lemma weights_mem_Icc {V : Type*} {k : Nat}
    [AddCommGroup V] [Module Real V]
    (x : V) {a : Fin k -> Real} {y : Fin k -> V}
    (h : ConvexCombination x a y) : a ∈ Set.Icc 0 1 := by
  simp only [Set.mem_Icc]
  refine ⟨h.1, ?_⟩
  intro i
  simp only [Pi.one_apply]
  rw [← h.2.1]
  exact Finset.single_le_sum (fun j _ => h.1 j) (Finset.mem_univ i)

lemma caratheodory_fixedLength {V : Type*}
    [NormedAddCommGroup V] [NormedSpace Real V] [FiniteDimensional Real V]
    (s : Set V) (k : Nat) (hk : k = Module.finrank Real V)
    {x : V} (hx : x ∈ convexHull Real s) :
    exists (z : Fin (k + 1) -> V) (a : Fin (k + 1) -> Real),
      Set.range z ⊆ s /\ ConvexCombination x a z := by
  obtain ⟨I, hI, z1, alpha, h⟩ := eq_pos_convex_span_of_mem_convexHull hx
  have hcard : hI.card <= k + 1 := by
    apply le_trans (AffineIndependent.card_le_finrank_succ h.2.1)
    rw [hk, add_le_add_iff_right]
    exact Submodule.finrank_le (vectorSpan Real (Set.range z1))
  let e := hI.equivFin
  let incl : Fin hI.card -> Fin (k + 1) := fun i => Fin.ofNat _ i.1
  let g := incl ∘ e
  have hg : Function.Injective g := by
    unfold g
    refine (Equiv.injective_comp e incl).mpr ?_
    intro i j hij
    unfold incl at hij
    simp only [Fin.ofNat_eq_cast] at hij
    rw [← Fin.val_eq_val] at hij ⊢
    rwa [Fin.val_cast_of_lt, Fin.val_cast_of_lt] at hij
    exact lt_of_lt_of_le j.2 hcard
    exact lt_of_lt_of_le i.2 hcard
  obtain ⟨s0, hs0⟩ : s.Nonempty := convexHull_nonempty_iff.mp ⟨x, hx⟩
  let beta := Function.extend g alpha (fun _ => 0)
  let z2 := Function.extend g z1 (fun _ => s0)
  have hz2 : Set.range z2 ⊆ s := by
    intro y hy
    obtain ⟨i, rfl⟩ := hy
    unfold z2
    by_cases hi : exists j, g j = i
    · obtain ⟨j, rfl⟩ := hi
      rw [Function.Injective.extend_apply hg]
      exact h.1 ⟨j, rfl⟩
    · simpa [Function.extend_apply' _ _ _ hi] using hs0
  refine ⟨z2, beta, hz2, ?_⟩
  have hsum : ∑ i, beta i = 1 := by
    rw [← h.2.2.2.1]
    symm
    apply Fintype.sum_of_injective g hg
    · exact fun i hi => Function.extend_apply' alpha (fun _ => 0) i hi
    · exact fun i => (Function.Injective.extend_apply hg alpha (fun _ => 0) i).symm
  have hrepr : x = ∑ i, beta i • z2 i := by
    rw [← h.2.2.2.2]
    apply Fintype.sum_of_injective g hg
    · intro i hi
      simp only [smul_eq_zero]
      exact Or.inl (Function.extend_apply' alpha (fun _ => 0) i hi)
    · intro i
      unfold beta z2
      rw [Function.Injective.extend_apply hg, Function.Injective.extend_apply hg]
  have hbeta : 0 <= beta := by
    unfold beta
    exact Function.extend_nonneg (fun j => (h.2.2.1 j).le) (by rfl)
  exact ⟨hbeta, hsum, hrepr⟩

/-- A finite partition of unity gives simplex-valued barycentric coordinates
whose synthesis approximates the identity. -/
lemma exists_simplexApproximation {V : Type*}
    [NormedAddCommGroup V] [NormedSpace Real V]
    (K : Set V) (hne : K.Nonempty) (hcompact : IsCompact K)
    {delta : Real} (hdelta : 0 < delta) :
    exists (m : PNat) (c : Fin m -> V) (q : K -> stdSimplex Real (Fin m)),
      (forall i, c i ∈ K) /\ Continuous q /\
      forall x : K, dist (∑ i, (q x).1 i • c i) x < delta := by
  obtain ⟨centersSet, hcentersK, hcentersFinite, hcover⟩ :=
    hcompact.finite_cover_balls hdelta
  let centers : Finset V := hcentersFinite.toFinset
  have hcenters_ne : centers.Nonempty := by
    obtain ⟨x, hx⟩ := hne
    obtain ⟨y, hy, _⟩ := Set.mem_iUnion₂.1 (hcover hx)
    exact ⟨y, by simpa [centers] using hy⟩
  let m : PNat := ⟨centers.card, Finset.card_pos.mpr hcenters_ne⟩
  let e : centers ≃ Fin m := centers.equivFin
  let c : Fin m -> V := fun i => (e.symm i : V)
  let U : Fin m -> Set K := fun i => Subtype.val ⁻¹' Metric.ball (c i) delta
  have hUopen : forall i, IsOpen (U i) := fun i =>
    Metric.isOpen_ball.preimage continuous_subtype_val
  have hcover' : (Set.univ : Set K) ⊆ ⋃ i, U i := by
    intro x _
    obtain ⟨y, hy, hxy⟩ := Set.mem_iUnion₂.1 (hcover x.property)
    have hyc : y ∈ centers := by simpa [centers] using hy
    let iy : Fin m := e ⟨y, hyc⟩
    exact Set.mem_iUnion.2 ⟨iy, by simpa [U, c, iy] using hxy⟩
  letI : CompactSpace K := isCompact_iff_compactSpace.mp hcompact
  obtain ⟨w, hwsub, hwsum, hwnonneg, _⟩ :=
    exists_continuous_sum_one_of_isOpen_isCompact hUopen isCompact_univ hcover'
  let q : K -> stdSimplex Real (Fin m) := fun x =>
    ⟨fun i => w i x, fun i => (hwnonneg i x).1,
      by simpa only [Finset.sum_apply, Pi.one_apply] using hwsum (Set.mem_univ x)⟩
  refine ⟨m, c, q, ?_, ?_, ?_⟩
  · intro i
    apply hcentersK
    have hi : (e.symm i : V) ∈ centers := (e.symm i).property
    change (e.symm i : V) ∈ centersSet
    simpa only [centers, hcentersFinite.mem_toFinset] using hi
  · apply Continuous.subtype_mk
    fun_prop
  · intro x
    have hsum : ∑ i, w i x = 1 := by
      simpa only [Finset.sum_apply, Pi.one_apply] using hwsum (Set.mem_univ x)
    have hsub : (∑ i, (q x).1 i • c i) - x = ∑ i, w i x • (c i - x) := by
      change (∑ i, w i x • c i) - x = _
      calc
        (∑ i, w i x • c i) - x =
            (∑ i, w i x • c i) - (∑ i, w i x) • (x : V) := by
              rw [hsum, one_smul]
        _ = ∑ i, (w i x • c i - w i x • (x : V)) := by
          rw [Finset.sum_sub_distrib, Finset.sum_smul]
        _ = ∑ i, w i x • (c i - x) := by simp only [smul_sub]
    rw [dist_eq_norm, hsub]
    calc
      ‖∑ i, w i x • (c i - x)‖ <= ∑ i, ‖w i x • (c i - x)‖ :=
        norm_sum_le _ _
      _ = ∑ i, w i x * ‖c i - x‖ := by
        apply Finset.sum_congr rfl
        intro i _
        rw [norm_smul, Real.norm_eq_abs, abs_of_nonneg (hwnonneg i x).1]
      _ < delta := by
        calc
          ∑ i, w i x * ‖c i - x‖ < ∑ i, w i x * delta := by
            apply Finset.sum_lt_sum
            · intro i _
              by_cases hwi : w i x = 0
              · simp only [hwi, zero_mul]; exact le_rfl
              · have hxU : x ∈ U i := hwsub i (subset_closure hwi)
                have hd : dist (c i) x < delta := by
                  simpa only [U, Set.mem_preimage, Metric.mem_ball, dist_comm] using hxU
                exact (mul_lt_mul_of_pos_left (by simpa [dist_eq_norm] using hd)
                  (lt_of_le_of_ne (hwnonneg i x).1 (Ne.symm hwi))).le
            · have hp : 0 < ∑ i, w i x := by rw [hsum]; exact zero_lt_one
              have hex : ∃ i ∈ (Finset.univ : Finset (Fin m)), 0 < w i x := by
                by_contra hnot
                push Not at hnot
                have hz : ∑ i, w i x <= 0 :=
                  Finset.sum_nonpos fun i _ => hnot i (Finset.mem_univ i)
                exact (not_lt_of_ge hz) hp
              obtain ⟨i, _, hwi⟩ := hex
              refine ⟨i, Finset.mem_univ _, ?_⟩
              have hxU : x ∈ U i := hwsub i (subset_closure hwi.ne')
              have hd : dist (c i) x < delta := by
                simpa only [U, Set.mem_preimage, Metric.mem_ball, dist_comm] using hxU
              exact mul_lt_mul_of_pos_left (by simpa [dist_eq_norm] using hd) hwi
          _ = delta := by simp only [← Finset.sum_mul, hsum, one_mul]

/-- Brouwer on the standard simplex yields the compact-convex Schauder theorem
needed by the Kakutani approximation. -/
lemma schauderFixedPoint {V : Type*}
    [NormedAddCommGroup V] [NormedSpace Real V]
    (K : Set V) (f : V -> V) (hne : K.Nonempty) (hcompact : IsCompact K)
    (hconv : Convex Real K) (hcont : ContinuousOn f K) (hmap : MapsTo f K K) :
    exists x, x ∈ K /\ f x = x := by
  have happrox : forall eps : Real, 0 < eps ->
      exists x, x ∈ K /\ dist (f x) x < eps := by
    intro eps heps
    obtain ⟨m, c, q, hcK, hqcont, hqclose⟩ :=
      exists_simplexApproximation K hne hcompact heps
    let r : stdSimplex Real (Fin m) -> V := fun a => ∑ i, a.1 i • c i
    have hrK : forall a, r a ∈ K := by
      intro a
      exact hconv.sum_mem (fun i _ => a.2.1 i) a.2.2 (fun i _ => hcK i)
    have hrcont : Continuous r := by
      apply continuous_finset_sum Finset.univ
      intro i _
      exact ((continuous_apply i).comp continuous_subtype_val).smul continuous_const
    let g : stdSimplex Real (Fin m) -> stdSimplex Real (Fin m) := fun a =>
      q ⟨f (r a), hmap (hrK a)⟩
    have hgcont : Continuous g := by
      apply hqcont.comp
      apply Continuous.subtype_mk
      exact hcont.comp_continuous hrcont hrK
    obtain ⟨a, ha⟩ := Brouwer g hgcont
    refine ⟨r a, hrK a, ?_⟩
    have hclose := hqclose ⟨f (r a), hmap (hrK a)⟩
    have hreconstruct : (∑ i, (q ⟨f (r a), hmap (hrK a)⟩).1 i • c i) = r a := by
      change r (g a) = r a
      rw [ha]
    rw [hreconstruct] at hclose
    simpa [dist_comm] using hclose
  obtain ⟨x, hxK, hxMin⟩ := hcompact.exists_isMinOn hne
    (fun y hy => (hcont y hy).dist continuousWithinAt_id)
  have hxZero : dist (f x) x = 0 := by
    apply le_antisymm
    · by_contra hnot
      have hxPos : 0 < dist (f x) x := lt_of_not_ge hnot
      obtain ⟨y, hyK, hy⟩ := happrox (dist (f x) x) hxPos
      exact (not_lt_of_ge (hxMin hyK)) hy
    · exact dist_nonneg
  exact ⟨x, hxK, dist_eq_zero.mp hxZero⟩

lemma correspondence_approximate_fixedPoint {V : Type*}
    [NormedAddCommGroup V] [NormedSpace Real V] [FiniteDimensional Real V]
    (K : Set V) (hcompact : IsCompact K) (hconv : Convex Real K)
    (hne : K.Nonempty) (f : K -> Set V)
    (hf : forall x, f x ⊆ K /\ Convex Real (f x) /\ (f x).Nonempty)
    (k : Nat) (hk : k = Module.finrank Real V)
    (eps : Real) (heps : 0 < eps) :
    exists a : K, exists y : Fin (k + 1) -> K,
      exists z : Fin (k + 1) -> V, exists alpha : Fin (k + 1) -> Real,
        ConvexCombination a.1 alpha z /\
        forall i, dist a (y i) < eps /\ z i ∈ f (y i) := by
  let G : K -> Set V := fun x =>
    convexHull Real {z | exists y : K, dist x y < eps /\ z ∈ f y}
  have hGconv : forall x, Convex Real (G x) := fun _ => convex_convexHull _ _
  letI : CompactSpace K := isCompact_iff_compactSpace.mp hcompact
  obtain ⟨g, hg⟩ : exists g : C(K, V), forall x, g x ∈ G x := by
    apply exists_continuous_forall_mem_convex_of_local_const hGconv
    intro x
    obtain ⟨z, hz⟩ := (hf x).2.2
    refine ⟨z, Metric.eventually_nhds_iff.mpr ⟨eps, heps, ?_⟩⟩
    intro y hy
    apply subset_convexHull
    exact ⟨x, by simpa [dist_comm] using hy, hz⟩
  have hgK : forall x, g x ∈ K := by
    intro x
    apply (convexHull_min _ hconv) (hg x)
    intro z hz
    obtain ⟨y, _, hzy⟩ := hz
    exact (hf y).1 hzy
  let gK : K -> K := fun x => ⟨g x, hgK x⟩
  have hgKcont : Continuous gK := Continuous.subtype_mk g.continuous hgK
  obtain ⟨a, haK, ha⟩ := schauderFixedPoint
    K (fun x : V => if hx : x ∈ K then (gK ⟨x, hx⟩ : V) else x)
    hne hcompact hconv (by
      intro x hx
      have heq : (fun y : K =>
          if hy : (y : V) ∈ K then (gK ⟨y, hy⟩ : V) else y) =
          fun y : K => (gK y : V) := by
        funext y
        simp only [dif_pos y.2]
      rw [continuousWithinAt_iff_continuousAt_restrict _ hx]
      rw [show K.restrict (fun x : V =>
          if hx : x ∈ K then (gK ⟨x, hx⟩ : V) else x) =
          (fun y : K => if hy : (y : V) ∈ K then (gK ⟨y, hy⟩ : V) else y) by rfl,
        heq]
      exact continuous_subtype_val.continuousAt.comp hgKcont.continuousAt)
    (by intro x hx; simp only [dif_pos hx]; exact hgK ⟨x, hx⟩)
  let aK : K := ⟨a, haK⟩
  have hga : a ∈ G aK := by
    rw [← ha]
    simpa only [dif_pos haK, aK, gK] using hg aK
  obtain ⟨z, alpha, hzG, hcomb⟩ := caratheodory_fixedLength _ k hk hga
  have hpoint : forall i, exists y : K, dist a y < eps /\ z i ∈ f y := by
    intro i
    exact hzG ⟨i, rfl⟩
  choose y hy using hpoint
  exact ⟨aK, y, z, alpha, hcomb, hy⟩

/-- The frozen closed-graph core, proved without any placeholder or bodyless
declaration. -/
theorem closedGraphKakutaniCore : ClosedGraphKakutaniCore := by
  intro n K F hne hcompact hconv hnonempty _hclosed hvalueConvex hmaps hgraph
  let f : K -> Set (E n) := fun x => F x.1
  have hf : forall x, f x ⊆ K /\ Convex Real (f x) /\ (f x).Nonempty := by
    intro x
    exact ⟨hmaps x x.2, hvalueConvex x x.2, hnonempty x x.2⟩
  let k := Module.finrank Real (E n)
  have happ := correspondence_approximate_fixedPoint K hcompact hconv hne f hf k rfl
  have heps (i : Nat) : 0 < (1 : Real) / (i + 1) := Nat.one_div_pos_of_nat
  have hex (i : Nat) := happ ((1 : Real) / (i + 1)) (heps i)
  have hpack i := Prod.exists'.mpr (Prod.exists'.mpr (Prod.exists'.mpr (hex i)))
  obtain ⟨B, hB⟩ := Classical.axiomOfChoice hpack
  clear happ hex hpack
  let Pack := ((K × (Fin (k + 1) -> K)) × (Fin (k + 1) -> E n)) ×
    (Fin (k + 1) -> Real)
  let S : Set Pack := (Set.univ ×ˢ {z | forall i, z i ∈ K}) ×ˢ Set.Icc 0 1
  have hScompact : IsCompact S := by
    letI : CompactSpace K := isCompact_iff_compactSpace.mp hcompact
    apply IsCompact.prod
    · apply IsCompact.prod
      · exact isCompact_univ
      · exact isCompact_pi_infinite (fun _ => hcompact)
    · exact isCompact_Icc
  have hBmem : forall i, B i ∈ S := by
    intro i
    refine ⟨⟨trivial, ?_⟩, weights_mem_Icc _ (hB i).1⟩
    intro j
    exact (hf _).1 ((hB i).2 j).2
  obtain ⟨B0, _hB0, phi, hphi, hBlim⟩ := hScompact.isSeqCompact hBmem
  let A := B ∘ phi
  have hAlim : Tendsto A atTop (nhds B0) := hBlim
  let x i := (A i).1.1.1
  let y j i := (A i).1.1.2 j
  let z j i := (A i).1.2 j
  let alpha j i := (A i).2 j
  let x0 := B0.1.1.1
  have halpha j : Tendsto (alpha j) atTop (nhds (B0.2 j)) :=
    (continuous_apply j).seqContinuous (Tendsto.snd_nhds hAlim)
  have hz j : Tendsto (z j) atTop (nhds (B0.1.2 j)) :=
    (continuous_apply j).seqContinuous (Tendsto.fst_nhds hAlim).snd_nhds
  have hx : Tendsto x atTop (nhds x0) := (Tendsto.fst_nhds hAlim).fst_nhds.fst_nhds
  have hy j : Tendsto (y j) atTop (nhds x0) := by
    have hdist i : dist (x i) (y j i) < 1 / ((phi i : Nat) + 1) :=
      ((hB (phi i)).2 j).1
    apply tendsto_of_tendsto_of_dist hx
    apply squeeze_zero (fun _ => dist_nonneg) _
      tendsto_one_div_add_atTop_nhds_zero_nat
    intro i
    apply le_trans (hdist i).le
    simp only [one_div]
    apply inv_anti₀ (Nat.cast_add_one_pos i)
    simp only [add_le_add_iff_right, Nat.cast_le]
    exact hphi.le_apply
  have hvalue j : B0.1.2 j ∈ F x0.1 := by
    let yzj i := ((y j i).1, z j i)
    have hyz i : yzj i ∈ CorrespondenceGraph K F := by
      exact ⟨(y j i).2, ((hB (phi i)).2 j).2⟩
    have hyzlim : Tendsto yzj atTop (nhds (x0.1, B0.1.2 j)) := by
      exact Tendsto.prodMk_nhds ((continuous_subtype_val.tendsto x0).comp (hy j)) (hz j)
    exact (hgraph.isSeqClosed hyz hyzlim).2
  have hcomb : ConvexCombination x0.1 B0.2 B0.1.2 := by
    refine ⟨?_, ?_, ?_⟩
    · intro j
      exact ge_of_tendsto' (halpha j) (fun i => (hB (phi i)).1.1 j)
    · have hsum := tendsto_finset_sum Finset.univ (fun i _ => halpha i)
      have heq i : ∑ j, alpha j i = 1 := (hB (phi i)).1.2.1
      simp only [heq, tendsto_const_nhds_iff] at hsum
      exact hsum.symm
    · have heq i : x i = ∑ j, alpha j i • z j i := (hB (phi i)).1.2.2
      have hsum := tendsto_finset_sum Finset.univ
        (fun i _ => Tendsto.smul (halpha i) (hz i))
      simp only [← heq] at hsum
      have hxval : Tendsto (fun i => (x i).1) atTop (nhds x0.1) :=
        continuous_subtype_val.seqContinuous hx
      exact tendsto_nhds_unique hxval hsum
  exact ⟨x0.1, x0.2, mem_of_convexCombination _ hcomb _
    (hvalueConvex x0.1 x0.2) hvalue⟩

/-- The unchanged canonical Kakutani target. -/
theorem kakutaniFixedPoint : KakutaniFixedPointTarget :=
  root_of_closedGraph_packages closedGraphKakutaniCore upperHemicontinuityClosedGraphBridge

#print axioms kakutaniFixedPoint

assert_no_sorry Brouwer
assert_no_sorry closedGraphKakutaniCore
assert_no_sorry kakutaniFixedPoint
#print sorries Brouwer
#print sorries closedGraphKakutaniCore
#print sorries kakutaniFixedPoint

end

end Stage1Instances.THM_M_0320
