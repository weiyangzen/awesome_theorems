import «Stage1_Instances».«THM-M-1133».ObligationTree
import Mathlib.Analysis.Calculus.DerivativeTest
import Mathlib.Analysis.Calculus.ContDiff.Operations
import Mathlib.Analysis.Calculus.IteratedDeriv.Defs
import Mathlib.Analysis.Calculus.FDeriv.CompCLM
import Mathlib.Analysis.Calculus.Deriv.Mul

/-!
# THM-M-1133 proof execution

This module proves the frozen weak heat-equation maximum principle. It first
proves the strict subsolution case on the compact cylinder, then applies the
strict perturbation `u x t - epsilon * t` and passes its boundary estimate to
the original subsolution.
-/

noncomputable section

open Set Filter Topology
open scoped BigOperators

namespace Stage1Instances.THM_M_1133

/-- Classical regularity together with a strict forward heat inequality. -/
def IsClassicalStrictSubcaloricOn {n : Nat} (U : Set (Space n)) (T : Real)
    (u : Space n → Real → Real) : Prop :=
  (∀ x ∈ U, ∀ t ∈ Ioc 0 T,
      ContDiffAt Real 2 (fun y => u y t) x ∧
      ContDiffAt Real 1 (fun s => u x s) t) ∧
    ∀ x ∈ U, ∀ t ∈ Ioc 0 T,
      deriv (fun s => u x s) t - spatialLaplacian u x t < 0

/-- The maximum principle package for strict classical subsolutions. -/
def StrictSubsolutionMaximumPrinciple : Prop :=
  ∀ (n : Nat) (U : Set (Space n)) (T : Real) (u : Space n → Real → Real),
    U.Nonempty → IsOpen U → Bornology.IsBounded U → 0 < T →
    ContinuousOn (fun p : Space n × Real => u p.1 p.2) (ClosedCylinder U T) →
    IsClassicalStrictSubcaloricOn U T u →
    ∃ p ∈ ParabolicBoundary U T,
      ∀ q ∈ ClosedCylinder U T, u q.1 q.2 ≤ u p.1 p.2

/-- A twice continuously differentiable real function has nonpositive second
derivative at a local maximum. -/
theorem second_deriv_nonpos_of_localMax {f : ℝ → ℝ} {x : ℝ}
    (hmax : IsLocalMax f x) (hf : ContDiffAt ℝ 2 f x) : deriv (deriv f) x ≤ 0 := by
  have hderiv0 : deriv f x = 0 :=
    hmax.hasDerivAt_eq_zero (hf.differentiableAt two_ne_zero).hasDerivAt
  by_contra h
  have hmin := isLocalMin_of_deriv_deriv_pos (lt_of_not_ge h) hderiv0 hf.continuousAt
  exact h <| le_of_eq (by
    simpa using (show f =ᶠ[nhds x] fun _ => f x from by
      filter_upwards [hmax, hmin] with y hymax hymin using le_antisymm hymax hymin).deriv.deriv_eq)

/-- At a local maximum, every diagonal value of the second Frechet derivative
is nonpositive. -/
theorem iteratedFDeriv_diag_nonpos_of_localMax
    {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {f : E → ℝ} {x v : E} (hmax : IsLocalMax f x) (hf : ContDiffAt ℝ 2 f x) :
    iteratedFDeriv ℝ 2 f x (fun _ => v) ≤ 0 := by
  let g : ℝ → ℝ := fun s => f (x + s • v)
  have hgmax : IsLocalMax g 0 := by
    show ∀ᶠ s in nhds 0, g s ≤ g 0
    have hmap : Tendsto (fun s : ℝ => x + s • v) (nhds 0) (nhds x) := by
      have h := (show ContinuousAt (fun s : ℝ => x + s • v) 0 by fun_prop)
      have hx0 : (fun s : ℝ => x + s • v) 0 = x := by simp
      have heq : nhds ((fun s : ℝ => x + s • v) 0) = nhds x := by rw [hx0]
      rw [← heq]
      exact h
    exact hmap.eventually hmax |>.mono fun s hs => by simpa [g] using hs
  have hline : ContDiffAt ℝ 2 (fun s : ℝ => x + s • v) 0 := by fun_prop
  have hg : ContDiffAt ℝ 2 g 0 := by
    change ContDiffAt ℝ 2 (f ∘ fun s : ℝ => x + s • v) 0
    apply (show ContDiffAt ℝ 2 f (x + (0 : ℝ) • v) by simpa using hf).comp 0
    simpa using hline
  have hsec := second_deriv_nonpos_of_localMax hgmax hg
  have hfirst : deriv g =ᶠ[nhds 0] fun s => fderiv ℝ f (x + s • v) v := by
    have hmap : Tendsto (fun s : ℝ => x + s • v) (nhds 0) (nhds x) := by
      have h := (show ContinuousAt (fun s : ℝ => x + s • v) 0 by fun_prop)
      have hx0 : (fun s : ℝ => x + s • v) 0 = x := by simp
      have heq : nhds ((fun s : ℝ => x + s • v) 0) = nhds x := by rw [hx0]
      rw [← heq]
      exact h
    filter_upwards [hmap.eventually (hf.eventually (by norm_num)),
        hline.eventually (by norm_num)] with s hfs hls
    change deriv (fun r : ℝ => f (x + r • v)) s = _
    have hinner : HasDerivAt (fun r : ℝ => x + r • v) v s := by
      convert (hasDerivAt_id s).smul_const v |>.const_add x using 1 <;> simp
    exact ((hfs.differentiableAt (by norm_num)).hasFDerivAt.comp_hasDerivAt s hinner).deriv
  rw [hfirst.deriv_eq] at hsec
  have hdinner : HasDerivAt (fun s : ℝ => x + s • v) v 0 := by
    simpa only [one_smul] using
      ((hasDerivAt_id (𝕜 := ℝ) (x := (0 : ℝ))).smul_const v |>.const_add x)
  have hfdiff : DifferentiableAt ℝ (fderiv ℝ f) x :=
    (hf.fderiv_right (show (1 : WithTop ℕ∞) + 1 ≤ 2 by norm_num)).differentiableAt one_ne_zero
  have hc : HasDerivAt (𝕜 := ℝ) (fun s : ℝ => fderiv ℝ f (x + s • v))
      (fderiv ℝ (fderiv ℝ f) x v) 0 := by
    have hfderivAt0 : HasFDerivAt (fderiv ℝ f) (fderiv ℝ (fderiv ℝ f) x)
        (x + (0 : ℝ) • v) := by
      simpa only [zero_smul, add_zero] using hfdiff.hasFDerivAt
    have hc' : HasDerivAt ((fderiv ℝ f) ∘ fun s : ℝ => x + s • v)
        (fderiv ℝ (fderiv ℝ f) x v) 0 :=
      hfderivAt0.comp_hasDerivAt (0 : ℝ) hdinner
    simpa [Function.comp_def] using hc'
  have hsecond : HasDerivAt (𝕜 := ℝ) (fun s : ℝ => fderiv ℝ f (x + s • v) v)
      (fderiv ℝ (fderiv ℝ f) x v v) 0 := by
    have hv : HasDerivAt (fun _ : ℝ => v) 0 0 := hasDerivAt_const (𝕜 := ℝ) 0 v
    simpa using hc.clm_apply hv
  rw [hsecond.deriv] at hsec
  simpa [iteratedFDeriv_two_apply] using hsec

/-- The coordinate Laplacian is nonpositive at a spatial local maximum. -/
theorem spatialLaplacian_nonpos_of_localMax {n : Nat} {u : Space n → ℝ → ℝ}
    {x : Space n} {t : ℝ} (hmax : IsLocalMax (fun y => u y t) x)
    (hsmooth : ContDiffAt ℝ 2 (fun y => u y t) x) : spatialLaplacian u x t ≤ 0 := by
  apply Finset.sum_nonpos
  intro i hi
  have h := iteratedFDeriv_diag_nonpos_of_localMax hmax hsmooth
    (v := EuclideanSpace.single i 1)
  rw [iteratedFDeriv_two_apply] at h
  have hc : DifferentiableAt ℝ (fderiv ℝ (fun y => u y t)) x :=
    (hsmooth.fderiv_right (show (1 : WithTop ℕ∞) + 1 ≤ 2 by norm_num)).differentiableAt
      (by norm_num)
  have hu : DifferentiableAt ℝ
      (fun _ : Space n => EuclideanSpace.single i (1 : ℝ)) x := differentiableAt_const _
  rw [fderiv_clm_apply hc hu]
  simpa using h

/-- The two-sided derivative is nonnegative at a local maximum relative to
the left half-line. -/
theorem deriv_nonneg_of_isLocalMaxOn_Iic {f : ℝ → ℝ} {x : ℝ}
    (hlocal : IsLocalMaxOn f (Iic x) x) (hf : DifferentiableAt ℝ f x) : 0 ≤ deriv f x := by
  have hlocalOn : IsLocalMaxOn f (Icc (x - 1) x) x :=
    hlocal.on_subset Icc_subset_Iic_self
  have hneg : (-1 : Real) ∈ posTangentConeAt (Icc (x - 1) x) x := by
    apply mem_posTangentConeAt_of_frequently_mem
    have hsmall : Ioo (0 : Real) 1 ∈ nhdsWithin 0 (Ioi 0) := Ioo_mem_nhdsGT zero_lt_one
    exact (frequently_iff.2 fun hs => by
      obtain ⟨t, ht, hts⟩ := Filter.nonempty_of_mem (inter_mem hs hsmall)
      exact ⟨t, ht, by
        constructor <;> simp only [smul_eq_mul] <;> linarith [hts.1, hts.2]⟩)
  have hnonpos := hlocalOn.fderivWithin_nonpos hneg
  have hunique : UniqueDiffWithinAt Real (Icc (x - 1) x) x :=
    uniqueDiffOn_Icc (by linarith) |>.uniqueDiffWithinAt (right_mem_Icc.mpr (by linarith))
  rw [fderivWithin_eq_fderiv hunique hf] at hnonpos
  rw [fderiv_eq_smul_deriv] at hnonpos
  simpa using hnonpos

/-- A strict classical subsolution cannot attain its cylinder maximum away
from the parabolic boundary. -/
theorem strictSubsolutionMaximumPrinciple : StrictSubsolutionMaximumPrinciple := by
  intro n U T u hU hOpen hBounded hT hContinuous hSub
  have hcompact : IsCompact (ClosedCylinder U T) :=
    hBounded.isCompact_closure.prod isCompact_Icc
  have hnonempty : (ClosedCylinder U T).Nonempty := by
    rcases hU with ⟨x, hx⟩
    exact ⟨(x, 0), subset_closure hx, left_mem_Icc.mpr hT.le⟩
  obtain ⟨p, hpCyl, hpMax⟩ := hcompact.exists_isMaxOn hnonempty hContinuous
  refine ⟨p, ?_, hpMax⟩
  by_contra hpNotBoundary
  rcases hpCyl with ⟨hpClosure, hpTime⟩
  have hpU : p.1 ∈ U := by
    have hpNotBoundary' := hpNotBoundary
    simp only [ParabolicBoundary, mem_union, mem_prod, mem_singleton_iff,
      not_or, not_and] at hpNotBoundary'
    rw [hOpen.frontier_eq] at hpNotBoundary'
    by_contra hpNotU
    exact hpNotBoundary'.2 ⟨hpClosure, hpNotU⟩ hpTime
  have hpTimePos : 0 < p.2 := by
    by_contra hnpos
    have hpZero : p.2 = 0 := le_antisymm (not_lt.mp hnpos) hpTime.1
    apply hpNotBoundary
    left
    exact ⟨hpClosure, hpZero⟩
  have hspaceMax : IsLocalMax (fun x => u x p.2) p.1 := by
    have hpMax' := hpMax.on_preimage (fun x : Space n => (x, p.2))
    apply hpMax'.isLocalMax
    filter_upwards [hOpen.mem_nhds hpU] with y hy
    exact ⟨subset_closure hy, hpTime⟩
  have hLap : spatialLaplacian u p.1 p.2 ≤ 0 :=
    spatialLaplacian_nonpos_of_localMax hspaceMax
      (hSub.1 p.1 hpU p.2 ⟨hpTimePos, hpTime.2⟩).1
  have hTimeDeriv : 0 ≤ deriv (fun s => u p.1 s) p.2 := by
    by_cases hpTop : p.2 = T
    · have hpMaxIic : IsLocalMaxOn (fun s => u p.1 s) (Iic T) T := by
        have hpos : Ioi 0 ∈ nhdsWithin T (Iic T) :=
          mem_nhdsWithin_of_mem_nhds (Ioi_mem_nhds hT)
        have hbase : Iic T ∈ nhdsWithin T (Iic T) := self_mem_nhdsWithin
        filter_upwards [hpos, hbase] with s hs0 hsT
        have hsCyl : (p.1, s) ∈ ClosedCylinder U T :=
          ⟨hpClosure, ⟨hs0.le, hsT⟩⟩
        have hs : u p.1 s ≤ u p.1 p.2 := hpMax hsCyl
        rwa [hpTop] at hs
      simpa [hpTop] using deriv_nonneg_of_isLocalMaxOn_Iic hpMaxIic
        (hSub.1 p.1 hpU T ⟨hT, le_rfl⟩).2.differentiableAt_one
    · have hpLt : p.2 < T := lt_of_le_of_ne hpTime.2 hpTop
      have htimeMax : IsLocalMax (fun s => u p.1 s) p.2 := by
        have hpMax' := hpMax.on_preimage (fun s : ℝ => (p.1, s))
        apply hpMax'.isLocalMax
        filter_upwards [Ioo_mem_nhds hpTimePos hpLt] with s hs
        exact ⟨hpClosure, hs.1.le, hs.2.le⟩
      exact le_of_eq htimeMax.deriv_eq_zero.symm
  have hpde := hSub.2 p.1 hpU p.2 ⟨hpTimePos, hpTime.2⟩
  linarith

/-- Subtracting a time-linear function does not change the spatial
Laplacian. -/
lemma spatialLaplacian_sub_time (u : Space n → Real → Real) (ε x t) :
    spatialLaplacian (fun y s => u y s - ε * s) x t = spatialLaplacian u x t := by
  simp only [spatialLaplacian]
  congr 1
  funext i
  simp only [fderiv_sub_const]

/-- The time derivative of the strict perturbation is shifted by `epsilon`. -/
lemma deriv_sub_mul_id {f : Real → Real} {ε t : Real}
    (hf : DifferentiableAt Real f t) :
    deriv (fun s => f s - ε * s) t = deriv f t - ε := by
  convert deriv_sub hf ((differentiableAt_const ε).mul differentiableAt_id) using 1 <;> simp

/-- The parabolic boundary is contained in the closed cylinder. -/
lemma parabolicBoundary_subset_closedCylinder {n : Nat} {U : Set (Space n)} {T : Real}
    (hT : 0 ≤ T) : ParabolicBoundary U T ⊆ ClosedCylinder U T := by
  rintro ⟨x, t⟩ (hinit | hlat)
  · change x ∈ closure U ∧ t ∈ ({0} : Set Real) at hinit
    rw [mem_singleton_iff] at hinit
    exact ⟨hinit.1, ⟨hinit.2.ge, hinit.2.le.trans hT⟩⟩
  · exact ⟨frontier_subset_closure hlat.1, hlat.2⟩

/-- A nonempty spatial domain gives a nonempty initial face. -/
lemma parabolicBoundary_nonempty {n : Nat} {U : Set (Space n)} {T : Real}
    (hU : U.Nonempty) : (ParabolicBoundary U T).Nonempty := by
  obtain ⟨x, hx⟩ := hU
  exact ⟨(x, 0), Or.inl ⟨subset_closure hx, rfl⟩⟩

/-- The parabolic boundary of a bounded spatial domain is compact. -/
lemma parabolicBoundary_compact {n : Nat} {U : Set (Space n)} {T : Real}
    (hU : Bornology.IsBounded U) : IsCompact (ParabolicBoundary U T) := by
  have hclosure : IsCompact (closure U) := hU.isCompact_closure
  have hfrontier : IsCompact (frontier U) :=
    hclosure.of_isClosed_subset isClosed_frontier frontier_subset_closure
  exact (hclosure.prod isCompact_singleton).union (hfrontier.prod isCompact_Icc)

/-- A positive time-linear perturbation turns a weak subsolution into a
strict subsolution. -/
lemma perturb_isStrictSubcaloric {n : Nat} {U : Set (Space n)} {T ε : Real}
    {u : Space n → Real → Real} (hε : 0 < ε)
    (hu : IsClassicalSubcaloricOn U T u) :
    IsClassicalStrictSubcaloricOn U T (fun x t => u x t - ε * t) := by
  refine ⟨?_, ?_⟩
  · intro x hx t ht
    refine ⟨?_, ?_⟩
    · exact (hu.1 x hx t ht).1.sub contDiffAt_const
    · exact (hu.1 x hx t ht).2.sub (contDiffAt_const.mul contDiffAt_id)
  · intro x hx t ht
    have htDiff : DifferentiableAt Real (fun s => u x s) t :=
      (hu.1 x hx t ht).2.differentiableAt one_ne_zero
    rw [spatialLaplacian_sub_time]
    rw [deriv_sub_mul_id htDiff]
    linarith [hu.2 x hx t ht]

/-- The strict perturbation remains continuous on the closed cylinder. -/
lemma perturb_continuousOn {n : Nat} {U : Set (Space n)} {T ε : Real}
    {u : Space n → Real → Real}
    (hu : ContinuousOn (fun p : Space n × Real => u p.1 p.2) (ClosedCylinder U T)) :
    ContinuousOn (fun p : Space n × Real => u p.1 p.2 - ε * p.2)
      (ClosedCylinder U T) := by
  exact hu.sub (continuousOn_const.mul continuousOn_snd)

/-- Frozen `M1133-T-LIMIT`: strict perturbation and an epsilon estimate give
the full weak subsolution maximum principle. -/
theorem weakSubsolutionMaximumPrinciple : WeakSubsolutionMaximumPrinciple := by
  intro n U T u hU hOpen hBounded hT hContinuous hSub
  have hBoundaryCompact : IsCompact (ParabolicBoundary U T) :=
    parabolicBoundary_compact hBounded
  have hBoundaryNonempty : (ParabolicBoundary U T).Nonempty :=
    parabolicBoundary_nonempty hU
  have hBoundaryContinuous :
      ContinuousOn (fun p : Space n × Real => u p.1 p.2) (ParabolicBoundary U T) :=
    hContinuous.mono (parabolicBoundary_subset_closedCylinder hT.le)
  obtain ⟨b, hb, hbmax⟩ :=
    hBoundaryCompact.exists_isMaxOn hBoundaryNonempty hBoundaryContinuous
  refine ⟨b, hb, ?_⟩
  intro q hq
  apply le_of_forall_pos_le_add
  intro δ hδ
  have hTne : T ≠ 0 := ne_of_gt hT
  let ε : Real := δ / T
  have hε : 0 < ε := div_pos hδ hT
  obtain ⟨p, hpBoundary, hpmax⟩ :=
    strictSubsolutionMaximumPrinciple n U T (fun x t => u x t - ε * t)
      hU hOpen hBounded hT (perturb_continuousOn hContinuous)
      (perturb_isStrictSubcaloric hε hSub)
  have hpCylinder : p ∈ ClosedCylinder U T :=
    parabolicBoundary_subset_closedCylinder hT.le hpBoundary
  have hpTime : 0 ≤ p.2 := hpCylinder.2.1
  have hqTime : q.2 ≤ T := hq.2.2
  have hperturb := hpmax q hq
  have hpBoundaryMax : u p.1 p.2 ≤ u b.1 b.2 := hbmax hpBoundary
  change u q.1 q.2 - ε * q.2 ≤ u p.1 p.2 - ε * p.2 at hperturb
  change u q.1 q.2 ≤ u b.1 b.2 + δ
  have hεnonneg : 0 ≤ δ / T := hε.le
  have hptNonneg : 0 ≤ (δ / T) * p.2 := mul_nonneg hεnonneg hpTime
  have hqt : (δ / T) * q.2 ≤ δ := by
    calc
      (δ / T) * q.2 ≤ (δ / T) * T := mul_le_mul_of_nonneg_left hqTime hεnonneg
      _ = δ := div_mul_cancel₀ δ hTne
  linarith

/-- Exact root closure through the frozen obligation-tree composition. -/
theorem heatEquationWeakMaximumPrinciple : HeatEquationWeakMaximumPrinciple :=
  root_of_subsolutionMaximumPrinciple weakSubsolutionMaximumPrinciple

#print axioms second_deriv_nonpos_of_localMax
#print axioms iteratedFDeriv_diag_nonpos_of_localMax
#print axioms spatialLaplacian_nonpos_of_localMax
#print axioms deriv_nonneg_of_isLocalMaxOn_Iic
#print axioms strictSubsolutionMaximumPrinciple
#print axioms perturb_isStrictSubcaloric
#print axioms weakSubsolutionMaximumPrinciple
#print axioms heatEquationWeakMaximumPrinciple

end Stage1Instances.THM_M_1133
