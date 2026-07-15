import Statement
import ObligationTree
import Gametheory.Brouwer
import Mathlib.Analysis.Convex.PartitionOfUnity
import Mathlib.Analysis.Normed.Module.Convex
import Mathlib.Analysis.Convex.Topology
import Mathlib.Topology.UniformSpace.HeineCantor
import Mathlib.Topology.MetricSpace.Pseudo.Basic

/-!
# THM-M-0318: Schauder fixed-point proof

The finite-dimensional branch uses a partition of unity and the vendored
simplex Brouwer theorem. The compact-limit branch minimizes displacement on
the compact carrier. The final declarations consume the frozen obligation
interfaces and inhabit the unchanged canonical target.
-/

open Set Function

noncomputable section

namespace Stage1Instances.THM_M_0318

universe u

/-- A finite partition of unity gives simplex-valued barycentric coordinates
whose synthesis approximates the identity. -/
theorem exists_simplex_approximation
    (E : Type u) [NormedAddCommGroup E] [NormedSpace Real E]
    (K : Set E) (hne : K.Nonempty) (hcompact : IsCompact K)
    (_hconv : Convex Real K) {delta : Real} (hdelta : 0 < delta) :
    exists (m : PNat) (c : Fin m -> E)
      (q : K -> stdSimplex Real (Fin m)),
      (forall i, c i ∈ K) ∧ Continuous q ∧
      (forall x : K, dist (∑ i, (q x).1 i • c i) x < delta) := by
  classical
  obtain ⟨centersSet, hcentersK, hcentersFinite, hcover⟩ :=
    hcompact.finite_cover_balls hdelta
  let centers : Finset E := hcentersFinite.toFinset
  have hcenters_ne : centers.Nonempty := by
    obtain ⟨x, hx⟩ := hne
    obtain ⟨y, hy, _⟩ := Set.mem_iUnion₂.1 (hcover hx)
    exact ⟨y, by simpa [centers] using hy⟩
  let m : PNat := ⟨centers.card, Finset.card_pos.mpr hcenters_ne⟩
  let e : centers ≃ Fin m := centers.equivFin
  let c : Fin m -> E := fun i => (e.symm i : E)
  let U : Fin m -> Set K :=
    fun i => Subtype.val ⁻¹' Metric.ball (c i) delta
  have hUopen : forall i, IsOpen (U i) := fun i =>
    Metric.isOpen_ball.preimage continuous_subtype_val
  have hcover' : (Set.univ : Set K) ⊆ ⋃ i, U i := by
    intro x hx
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
    have hi : (e.symm i : E) ∈ centers := (e.symm i).property
    change (e.symm i : E) ∈ centersSet
    simpa only [centers, hcentersFinite.mem_toFinset] using hi
  · apply Continuous.subtype_mk
    fun_prop
  · intro x
    have hsum : ∑ i, w i x = 1 := by
      simpa only [Finset.sum_apply, Pi.one_apply] using hwsum (Set.mem_univ x)
    have hp_sub : (∑ i, (q x).1 i • c i) - x = ∑ i, w i x • (c i - x) := by
      change (∑ i, w i x • c i) - x = _
      calc
        (∑ i, w i x • c i) - x =
            (∑ i, w i x • c i) - (∑ i, w i x) • (x : E) := by rw [hsum, one_smul]
        _ = ∑ i, (w i x • c i - w i x • (x : E)) := by
          rw [Finset.sum_sub_distrib, Finset.sum_smul]
        _ = ∑ i, w i x • (c i - x) := by simp only [smul_sub]
    rw [dist_eq_norm, hp_sub]
    calc
      ‖∑ i, w i x • (c i - x)‖
          ≤ ∑ i, ‖w i x • (c i - x)‖ := norm_sum_le _ _
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
                have hdist : dist (c i) x < delta := by
                  simpa only [U, Set.mem_preimage, Metric.mem_ball, dist_comm]
                    using hxU
                exact (mul_lt_mul_of_pos_left (by simpa [dist_eq_norm] using hdist)
                  (lt_of_le_of_ne (hwnonneg i x).1 (Ne.symm hwi))).le
            · have hsum_pos : 0 < ∑ i, w i x := by rw [hsum]; exact zero_lt_one
              have hexists : ∃ i ∈ (Finset.univ : Finset (Fin m)), 0 < w i x := by
                by_contra hnot
                push Not at hnot
                have hzero : ∑ i, w i x ≤ 0 :=
                  Finset.sum_nonpos fun i _ => hnot i (Finset.mem_univ i)
                exact (not_lt_of_ge hzero) hsum_pos
              obtain ⟨i, _, hwi⟩ := hexists
              refine ⟨i, Finset.mem_univ _, ?_⟩
              have hxU : x ∈ U i := hwsub i (subset_closure hwi.ne')
              have hdist : dist (c i) x < delta := by
                simpa only [U, Set.mem_preimage, Metric.mem_ball, dist_comm]
                  using hxU
              exact mul_lt_mul_of_pos_left (by simpa [dist_eq_norm] using hdist) hwi
          _ = delta := by simp only [← Finset.sum_mul, hsum, one_mul]

theorem hasApproximateFixedPoints
    (E : Type u) [NormedAddCommGroup E] [NormedSpace Real E]
    (K : Set E) (f : E -> E) (hne : K.Nonempty) (hcompact : IsCompact K)
    (hconv : Convex Real K) (hcont : ContinuousOn f K)
    (hmap : MapsTo f K K) :
    forall epsilon : Real, 0 < epsilon ->
      exists x : E, x ∈ K ∧ dist (f x) x < epsilon := by
  intro epsilon hepsilon
  obtain ⟨m, c, q, hcK, hqcont, hqclose⟩ :=
    exists_simplex_approximation E K hne hcompact hconv hepsilon
  let r : stdSimplex Real (Fin m) -> E := fun a => ∑ i, a.1 i • c i
  have hrK : forall a, r a ∈ K := by
    intro a
    apply hconv.sum_mem
    · intro i _
      exact a.2.1 i
    · exact a.2.2
    · intro i _
      exact hcK i
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

/-- The construction and Brouwer branches supply the frozen approximation
engine without any additional assumptions. -/
theorem approximationEngine : ApproximationEngine.{u} := by
  intro E _ _ K f hne hcompact hconv hcont hmap
  exact hasApproximateFixedPoints E K f hne hcompact hconv hcont hmap

/-- Compact minimization of displacement turns approximate fixed points into
an exact fixed point without choosing a sequence. -/
theorem compactLimitEngine : CompactLimitEngine.{u} := by
  intro E _ _ K f hcompact hcont happrox
  have hne : K.Nonempty := by
    obtain ⟨x, hx, _⟩ := happrox 1 zero_lt_one
    exact ⟨x, hx⟩
  obtain ⟨x, hxK, hxMin⟩ := hcompact.exists_isMinOn
    hne (fun y hy => (hcont y hy).dist continuousWithinAt_id)
  have hxZero : dist (f x) x = 0 := by
    apply le_antisymm
    · by_contra hnot
      have hxPos : 0 < dist (f x) x := lt_of_not_ge hnot
      obtain ⟨y, hyK, hy⟩ := happrox (dist (f x) x) hxPos
      exact (not_lt_of_ge (hxMin hyK)) hy
    · exact dist_nonneg
  exact ⟨x, hxK, dist_eq_zero.mp hxZero⟩

/-- Checked composition through the exact interfaces frozen by the obligation
tree. -/
theorem exactSchauderTarget : ExactSchauderTarget.{u} :=
  compose_schauder approximationEngine compactLimitEngine

/-- The exact canonical statement from `Statement.lean`. -/
theorem schauderFixedPoint : SchauderFixedPointTarget.{u} := by
  exact exactSchauderTarget

end Stage1Instances.THM_M_0318

assert_no_sorry IndexedLOrder.Scarf
assert_no_sorry IndexedLOrder.GiComponentStructure_holds
assert_no_sorry Brouwer
assert_no_sorry Stage1Instances.THM_M_0318.exists_simplex_approximation
assert_no_sorry Stage1Instances.THM_M_0318.hasApproximateFixedPoints
assert_no_sorry Stage1Instances.THM_M_0318.approximationEngine
assert_no_sorry Stage1Instances.THM_M_0318.compactLimitEngine
assert_no_sorry Stage1Instances.THM_M_0318.exactSchauderTarget
assert_no_sorry Stage1Instances.THM_M_0318.schauderFixedPoint
#print sorries IndexedLOrder.Scarf
#print sorries IndexedLOrder.GiComponentStructure_holds
#print sorries Brouwer
#print sorries Stage1Instances.THM_M_0318.exists_simplex_approximation
#print sorries Stage1Instances.THM_M_0318.hasApproximateFixedPoints
#print sorries Stage1Instances.THM_M_0318.approximationEngine
#print sorries Stage1Instances.THM_M_0318.compactLimitEngine
#print sorries Stage1Instances.THM_M_0318.exactSchauderTarget
#print sorries Stage1Instances.THM_M_0318.schauderFixedPoint
#print axioms IndexedLOrder.Scarf
#print axioms IndexedLOrder.GiComponentStructure_holds
#print axioms Brouwer
#print axioms Stage1Instances.THM_M_0318.exists_simplex_approximation
#print axioms Stage1Instances.THM_M_0318.hasApproximateFixedPoints
#print axioms Stage1Instances.THM_M_0318.approximationEngine
#print axioms Stage1Instances.THM_M_0318.compactLimitEngine
#print axioms Stage1Instances.THM_M_0318.exactSchauderTarget
#print axioms Stage1Instances.THM_M_0318.schauderFixedPoint
