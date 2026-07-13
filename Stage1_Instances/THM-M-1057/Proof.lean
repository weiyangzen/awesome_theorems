import Statement
import ObligationTree
import KingmanMeans
import Mathlib.MeasureTheory.Function.AEMeasurableSequence

/-!
# THM-M-1057: Kingman's subadditive ergodic theorem

The target assumes subadditivity almost everywhere for each pair of indices,
whereas the imported Kingman theorem uses a pointwise cocycle.  The
strictification below intersects the countable family of good sets along all
forward iterates, then replaces the process and transformation by zero and the
identity off that invariant full-measure set.  This gives a pointwise cocycle
without changing any almost-everywhere conclusion or integral mean.
-/

noncomputable section

open Filter Function MeasureTheory Set
open scoped MeasureTheory Topology

namespace Stage1Instances.THM_M_1057

universe u

namespace Strictification

variable {Omega : Type u} [MeasurableSpace Omega] (P : KingmanData Omega)

private def indexedProcess : (Nat × Nat × Nat) -> Omega -> Real
  | (0, m, n), omega => P.process (m + n) omega
  | (1, m, _), omega => P.process m omega
  | (_, m, n), omega => P.process n ((P.transformation^[m]) omega)

private theorem indexedProcess_aemeasurable (i : Nat × Nat × Nat) :
    AEMeasurable (indexedProcess P i) P.measure := by
  rcases i with ⟨tag, m, n⟩
  rcases tag with _ | tag
  · exact (P.integrable (m + n)).aestronglyMeasurable.aemeasurable
  rcases tag with _ | tag
  · exact (P.integrable m).aestronglyMeasurable.aemeasurable
  · exact ((P.isErgodic.toMeasurePreserving.iterate m).integrable_comp_of_integrable
      (P.integrable n)).aestronglyMeasurable.aemeasurable

private def goodProperty (_omega : Omega) (f : (Nat × Nat × Nat) -> Real) : Prop :=
  forall m n, f (0, m, n) <= f (1, m, n) + f (2, m, n)

private theorem goodProperty_ae :
    ∀ᵐ omega ∂P.measure,
      goodProperty omega (fun i => indexedProcess P i omega) := by
  filter_upwards [ae_all_iff.2 fun m => ae_all_iff.2 fun n => P.subadditive m n]
      with omega hsub
  intro m n
  simpa [indexedProcess] using hsub m n

private def goodSet : Set Omega :=
  aeSeqSet (indexedProcess_aemeasurable P) goodProperty

private theorem measurableSet_goodSet : MeasurableSet (goodSet P) :=
  aeSeq.aeSeqSet_measurableSet

private theorem measure_compl_goodSet : P.measure (goodSet P)ᶜ = 0 :=
  aeSeq.measure_compl_aeSeqSet_eq_zero (indexedProcess_aemeasurable P) (goodProperty_ae P)

private theorem goodSet_subadditive {omega : Omega} (homega : omega ∈ goodSet P)
    (m n : Nat) :
    P.process (m + n) omega <=
      P.process m omega + P.process n ((P.transformation^[m]) omega) := by
  have h := aeSeq.fun_prop_of_mem_aeSeqSet (indexedProcess_aemeasurable P) homega m n
  simpa [goodProperty, indexedProcess] using h

private def stableSet : Set Omega :=
  ⋂ k : Nat, P.transformation^[k] ⁻¹' goodSet P

private theorem measurableSet_stableSet : MeasurableSet (stableSet P) := by
  exact MeasurableSet.iInter fun k => (measurableSet_goodSet P).preimage
    (P.isErgodic.measurable.iterate k)

private theorem measure_compl_stableSet : P.measure (stableSet P)ᶜ = 0 := by
  rw [stableSet, compl_iInter, measure_iUnion_null_iff]
  intro k
  exact (P.isErgodic.toMeasurePreserving.iterate k).preimage_null (measure_compl_goodSet P)

private theorem stableSet_subset_goodSet : stableSet P ⊆ goodSet P := by
  intro omega homega
  have := Set.mem_iInter.mp homega 0
  simpa using this

private theorem transformation_mem_stableSet {omega : Omega} (homega : omega ∈ stableSet P) :
    P.transformation omega ∈ stableSet P := by
  rw [stableSet] at homega ⊢
  refine Set.mem_iInter.mpr fun k => ?_
  have hk := Set.mem_iInter.mp homega (k + 1)
  simpa only [Set.mem_preimage, Function.iterate_succ_apply] using hk

private theorem iterate_mem_stableSet {omega : Omega} (homega : omega ∈ stableSet P) (m : Nat) :
    P.transformation^[m] omega ∈ stableSet P := by
  induction m with
  | zero => simpa using homega
  | succ m ih =>
      simpa only [Function.iterate_succ_apply'] using transformation_mem_stableSet P ih

private noncomputable def strictTransformation (omega : Omega) : Omega := by
  classical
  exact if omega ∈ stableSet P then P.transformation omega else omega

private theorem strictTransformation_measurable : Measurable (strictTransformation P) := by
  exact Measurable.ite (measurableSet_stableSet P) P.isErgodic.measurable measurable_id

private theorem strictTransformation_ae :
    strictTransformation P =ᵐ[P.measure] P.transformation := by
  filter_upwards [ae_iff.2 (measure_compl_stableSet P)] with omega homega
  simp [strictTransformation, homega]

private theorem preErgodic_congr {f g : Omega -> Omega} (hf : QuasiErgodic f P.measure)
    (hfg : f =ᵐ[P.measure] g) : PreErgodic g P.measure := by
  refine ⟨fun s hs hgs => ?_⟩
  apply hf.aeconst_set₀ hs.nullMeasurableSet
  exact (hfg.preimage s).trans (EventuallyEq.of_eq hgs)

private theorem strictTransformation_ergodic : Ergodic (strictTransformation P) P.measure where
  toMeasurePreserving := P.isErgodic.toMeasurePreserving.congr
    (strictTransformation_measurable P) (strictTransformation_ae P).symm
  toPreErgodic := preErgodic_congr P P.isErgodic.quasiErgodic
    (strictTransformation_ae P).symm

private noncomputable def strictProcess (n : Nat) (omega : Omega) : Real := by
  classical
  exact if omega ∈ stableSet P then P.process n omega else 0

private theorem strictProcess_ae (n : Nat) :
    strictProcess P n =ᵐ[P.measure] P.process n := by
  filter_upwards [ae_iff.2 (measure_compl_stableSet P)] with omega homega
  simp [strictProcess, homega]

private theorem strictProcess_integrable (n : Nat) :
    Integrable (strictProcess P n) P.measure :=
  (P.integrable n).congr (strictProcess_ae P n).symm

private theorem strictTransformation_iterate {omega : Omega} (homega : omega ∈ stableSet P)
    (m : Nat) :
    (strictTransformation P)^[m] omega = P.transformation^[m] omega := by
  induction m with
  | zero => rfl
  | succ m ih =>
      rw [Function.iterate_succ_apply', Function.iterate_succ_apply', ih]
      simp [strictTransformation, iterate_mem_stableSet P homega m]

private theorem strictTransformation_iterate_of_not_mem {omega : Omega}
    (homega : omega ∉ stableSet P) (m : Nat) :
    (strictTransformation P)^[m] omega = omega := by
  induction m with
  | zero => rfl
  | succ m ih =>
      rw [Function.iterate_succ_apply', ih]
      simp [strictTransformation, homega]

private theorem strictProcess_subadditive :
    ErgodicTheory.IsSubadditiveCocycle (strictTransformation P) (strictProcess P) := by
  refine ⟨fun m n omega => ?_⟩
  by_cases homega : omega ∈ stableSet P
  · rw [strictProcess, if_pos homega, strictProcess, if_pos homega,
        strictTransformation_iterate P homega]
    rw [strictProcess, if_pos (iterate_mem_stableSet P homega m)]
    exact goodSet_subadditive P (stableSet_subset_goodSet P homega) m n
  · rw [strictProcess, if_neg homega, strictProcess, if_neg homega,
        strictTransformation_iterate_of_not_mem P homega, strictProcess, if_neg homega]
    simp

private theorem integral_comp_iterate (m n : Nat) :
    (∫ omega, P.process n ((P.transformation^[m]) omega) ∂P.measure) =
      ∫ omega, P.process n omega ∂P.measure := by
  have hmp := P.isErgodic.toMeasurePreserving.iterate m
  have haesm : AEStronglyMeasurable (P.process n) (Measure.map (P.transformation^[m]) P.measure) := by
    rw [hmp.map_eq]
    exact (P.integrable n).aestronglyMeasurable
  have hmap := integral_map (μ := P.measure) (φ := P.transformation^[m])
    hmp.aemeasurable (f := P.process n) haesm
  rw [hmp.map_eq] at hmap
  exact hmap.symm

private theorem integral_subadditive :
    Subadditive (fun n => ∫ omega, P.process n omega ∂P.measure) := by
  intro m n
  have hcomp : Integrable (fun omega => P.process n ((P.transformation^[m]) omega)) P.measure :=
    (P.isErgodic.toMeasurePreserving.iterate m).integrable_comp_of_integrable (P.integrable n)
  calc
    (∫ omega, P.process (m + n) omega ∂P.measure)
        <= ∫ omega, P.process m omega + P.process n ((P.transformation^[m]) omega) ∂P.measure :=
      integral_mono_ae (P.integrable (m + n)) ((P.integrable m).add hcomp) (P.subadditive m n)
    _ = (∫ omega, P.process m omega ∂P.measure) +
        ∫ omega, P.process n ((P.transformation^[m]) omega) ∂P.measure :=
      integral_add (P.integrable m) hcomp
    _ = (∫ omega, P.process m omega ∂P.measure) +
        ∫ omega, P.process n omega ∂P.measure := by rw [integral_comp_iterate P m n]

private theorem normalized_bddBelow :
    BddBelow (Set.range fun n : Nat =>
      (∫ omega, strictProcess P (n + 1) omega ∂P.measure) / (n + 1)) := by
  obtain ⟨C, hC⟩ := P.normalizedExpectationsBoundedBelow
  refine ⟨C, ?_⟩
  rintro y ⟨n, rfl⟩
  change C ≤ (∫ omega, strictProcess P (n + 1) omega ∂P.measure) / (n + 1)
  rw [integral_congr_ae (strictProcess_ae P (n + 1))]
  simpa only [Nat.cast_add, Nat.cast_one] using hC (n + 1) (Nat.succ_ne_zero n)

private theorem all_normalized_bddBelow :
    BddBelow (Set.range fun n : Nat =>
      (∫ omega, P.process n omega ∂P.measure) / n) := by
  obtain ⟨C, hC⟩ := P.normalizedExpectationsBoundedBelow
  refine ⟨min C 0, ?_⟩
  rintro y ⟨n, rfl⟩
  rcases n with _ | n
  · simp
  · exact (min_le_left C 0).trans (hC (n + 1) (Nat.succ_ne_zero n))

private theorem integral_mean_tendsto_value :
    Tendsto (fun n : Nat =>
      (∫ omega, strictProcess P (n + 1) omega ∂P.measure) / (n + 1)) atTop
      (nhds (kingmanValue P)) := by
  have hlim := (integral_subadditive P).tendsto_lim (all_normalized_bddBelow P)
  rw [← tendsto_add_atTop_iff_nat (f := fun n : Nat =>
    (∫ omega, P.process n omega ∂P.measure) / n) 1] at hlim
  have hshift : Tendsto (fun n : Nat =>
      (∫ omega, P.process (n + 1) omega ∂P.measure) / (n + 1)) atTop
      (nhds ((integral_subadditive P).lim)) := by
    exact hlim.congr fun n => by push_cast; rfl
  have hvalue : (integral_subadditive P).lim = kingmanValue P := by
    rw [Subadditive.lim]
    rfl
  rw [hvalue] at hshift
  exact hshift.congr fun n => by
    rw [integral_congr_ae (strictProcess_ae P (n + 1))]

private theorem strictProcess_ae_all :
    ∀ᵐ omega ∂P.measure, forall n, strictProcess P n omega = P.process n omega :=
  ae_all_iff.2 (strictProcess_ae P)

end Strictification

theorem pointwiseLimitPackage : PointwiseLimitPackage.{u} := by
  intro Omega _ P
  letI : IsProbabilityMeasure P.measure := P.isProbability
  obtain ⟨c, hcMeans, hcPointwise⟩ :=
    ErgodicTheory.tendsto_kingman_ergodic_means
      (Strictification.strictTransformation_ergodic P)
      (Strictification.strictProcess_subadditive P)
      (Strictification.strictProcess_integrable P)
      (Strictification.normalized_bddBelow P)
  have hc : c = kingmanValue P :=
    tendsto_nhds_unique hcMeans (Strictification.integral_mean_tendsto_value P)
  refine ⟨fun _ => kingmanValue P, ?_, Eventually.of_forall fun _ => rfl,
    Eventually.of_forall fun _ => rfl⟩
  filter_upwards [hcPointwise, Strictification.strictProcess_ae_all P] with omega hconv heq
  rw [hc] at hconv
  have hconv' : Tendsto (fun n : Nat => (n : Real)⁻¹ * P.process n omega) atTop
      (nhds (kingmanValue P)) := hconv.congr' (Eventually.of_forall fun n => by rw [heq n])
  simpa only [normalizedProcess, div_eq_inv_mul] using hconv'

theorem kingmanTarget : KingmanTarget.{u} :=
  root_of_pointwiseLimitPackage pointwiseLimitPackage

#print sorries ErgodicTheory.tendsto_kingman_ergodic_means
#print sorries pointwiseLimitPackage
#print sorries kingmanTarget
#print axioms pointwiseLimitPackage
#print axioms kingmanTarget

end Stage1Instances.THM_M_1057
