import Mathlib.Analysis.Calculus.LocalExtr.Basic
import Mathlib.Analysis.Calculus.DerivativeTest
import Mathlib.Analysis.Calculus.IteratedDeriv.FaaDiBruno
import Mathlib.Analysis.InnerProductSpace.Laplacian
import Mathlib.Topology.MetricSpace.Bounded
import Mathlib.Topology.Order.Compact
import Statement
import ObligationTree

/-!
# THM-M-1188 proof execution

This module proves the frozen weak maximum principle by applying a strict
time perturbation on truncated cylinders and passing to the terminal face by
continuity.
-/

namespace Stage1Instances.THM_M_1188.Proof

open Set Filter
open scoped InnerProductSpace

abbrev Euclidean (n : Nat) := EuclideanSpace Real (Fin n)

def closedCylinder {n : Nat} (U : Set (Euclidean n)) (T : Real) :
    Set (Euclidean n × Real) :=
  closure U ×ˢ Set.Icc 0 T

def parabolicBoundary {n : Nat} (U : Set (Euclidean n)) (T : Real) :
    Set (Euclidean n × Real) :=
  (closure U ×ˢ ({0} : Set Real)) ∪ (frontier U ×ˢ Set.Icc 0 T)

/-- A twice continuously differentiable real function has nonpositive second
derivative at a local maximum.  Mathlib supplies the converse derivative test;
the short argument below rules out a positive second derivative by observing
that simultaneous local maximum and minimum force local constancy. -/
theorem iteratedDeriv_two_nonpos_of_isLocalMax {f : Real → Real} {x : Real}
    (hmax : IsLocalMax f x) (hf : ContDiffAt Real 2 f x) :
    iteratedDeriv 2 f x ≤ 0 := by
  by_contra hnot
  have hpositive : 0 < iteratedDeriv 2 f x := lt_of_not_ge hnot
  have hfirst : deriv f x = 0 := hmax.deriv_eq_zero
  have hsecond : 0 < deriv (deriv f) x := by
    simpa [iteratedDeriv_succ] using hpositive
  have hmin : IsLocalMin f x :=
    isLocalMin_of_deriv_deriv_pos hsecond hfirst hf.continuousAt
  have heq : f =ᶠ[nhds x] fun _ ↦ f x := by
    filter_upwards [hmax, hmin] with y hymax hymin
    exact le_antisymm hymax hymin
  have hzero : deriv (deriv f) x = 0 := by
    have hderiv : deriv f =ᶠ[nhds x] deriv (fun _ ↦ f x) := heq.deriv
    have hderiv2 := hderiv.deriv_eq
    simpa using hderiv2
  exact hsecond.ne' hzero

/-- The second derivative of a spatial function along a line is the Hessian
applied twice to the line direction. -/
theorem directional_second_eq
    {E : Type*} [NormedAddCommGroup E] [NormedSpace Real E]
    {f : E → Real} {x v : E} (hf : ContDiffAt Real 2 f x) :
    deriv (deriv (fun r : Real ↦ f (x + r • v))) 0 =
      iteratedFDeriv Real 2 f x ![v, v] := by
  let L : Real →L[Real] E := ContinuousLinearMap.toSpanSingleton Real v
  let q : Real → E := fun r ↦ x + L r
  let g : Real → Real := fun r ↦ f (q r)
  have hqzero : q 0 = x := by simp [q]
  have hq : HasFDerivAt q L 0 := by
    simpa [q] using L.hasFDerivAt.const_add x
  have hfev : ∀ᶠ y in nhds x, DifferentiableAt Real f y := by
    filter_upwards [hf.eventually (by norm_num)] with y hy
    exact hy.differentiableAt (by norm_num)
  have hqnhds : Tendsto q (nhds 0) (nhds x) := by
    rw [← hqzero]
    exact hq.continuousAt
  have hfirst : deriv g =ᶠ[nhds 0] fun r ↦ fderiv Real f (q r) v := by
    filter_upwards [hqnhds.eventually hfev] with r hfr
    have hqc : HasDerivAt q v r := by
      simpa [q, L] using L.hasDerivAt.const_add x
    simpa [g] using (hfr.hasFDerivAt.comp r hqc.hasFDerivAt).hasDerivAt.deriv
  change deriv (deriv g) 0 = _
  rw [hfirst.deriv_eq]
  have hDf : DifferentiableAt Real (fderiv Real f) x :=
    hf.fderiv_right (m := 1) (by norm_num) |>.differentiableAt (by norm_num)
  have hc : HasFDerivAt (fun r ↦ fderiv Real f (q r))
      ((fderiv Real (fderiv Real f) x).comp L) 0 := by
    have hDf' : HasFDerivAt (fderiv Real f)
        (fderiv Real (fderiv Real f) x) (q 0) := by
      simpa [hqzero] using hDf.hasFDerivAt
    simpa [hqzero] using hDf'.comp 0 hq
  have hv : HasFDerivAt (fun _ : Real ↦ v) (0 : Real →L[Real] E) 0 := by
    fun_prop
  have hk := hc.clm_apply hv
  have hk' := hk.hasDerivAt.deriv
  rw [iteratedFDeriv_two_apply]
  simpa [q, L, hqzero] using hk'

/-- The spatial Laplacian is nonpositive at a `C2` local maximum.  This closes
the substantive sign statement of frozen obligation `M1188-L-SPATIAL`. -/
theorem laplacian_nonpos_of_isLocalMax
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace Real E]
    [FiniteDimensional Real E] {f : E → Real} {x : E}
    (hmax : IsLocalMax f x) (hf : ContDiffAt Real 2 f x) :
    Laplacian.laplacian f x ≤ 0 := by
  rw [InnerProductSpace.laplacian_eq_iteratedFDeriv_stdOrthonormalBasis]
  apply Finset.sum_nonpos
  intro i _hi
  let v := (stdOrthonormalBasis Real E) i
  let g : Real → Real := fun r ↦ f (x + r • v)
  have hgmax : IsLocalMax g 0 := by
    have hc : ContinuousAt (fun r : Real ↦ x + r • v) 0 := by fun_prop
    have hh : IsLocalMax f (x + (0 : Real) • v) := by simpa using hmax
    have hh' : IsLocalMax (f ∘ fun r : Real ↦ x + r • v) 0 :=
      IsLocalMax.comp_continuous hh hc
    simpa [g, Function.comp_def] using hh'
  have hgdiff : ContDiffAt Real 2 g 0 := by
    have hf' : ContDiffAt Real 2 f (x + (0 : Real) • v) := by simpa using hf
    have hh := hf'.comp 0
      (show ContDiffAt Real 2 (fun r : Real ↦ x + r • v) 0 by fun_prop)
    simpa [g, Function.comp_def] using hh
  have hsign := iteratedDeriv_two_nonpos_of_isLocalMax hgmax hgdiff
  rw [show iteratedDeriv 2 g 0 = iteratedFDeriv Real 2 f x ![v, v] by
    simpa [iteratedDeriv_succ, g] using directional_second_eq hf] at hsign
  simpa [v] using hsign

/-- The frozen closed cylinder is compact under the target's bounded-domain
hypothesis.  This is the compactness component of `M1188-C-COMPACT`. -/
theorem closedCylinder_isCompact {n : Nat} {U : Set (Euclidean n)} {T : Real}
    (hU : Bornology.IsBounded U) : IsCompact (closedCylinder U T) := by
  exact hU.isCompact_closure.prod isCompact_Icc

/-- A nonempty spatial domain and nonnegative terminal time make the closed
cylinder nonempty. -/
theorem closedCylinder_nonempty {n : Nat} {U : Set (Euclidean n)} {T : Real}
    (hU : U.Nonempty) (hT : 0 ≤ T) : (closedCylinder U T).Nonempty := by
  obtain ⟨x, hx⟩ := hU
  exact ⟨(x, 0), subset_closure hx, left_mem_Icc.mpr hT⟩

/-- The exact parabolic boundary is a closed subset of the compact cylinder,
so it is compact. -/
theorem parabolicBoundary_isCompact {n : Nat} {U : Set (Euclidean n)} {T : Real}
    (hU : Bornology.IsBounded U) (hT : 0 ≤ T) :
    IsCompact (parabolicBoundary U T) := by
  apply (closedCylinder_isCompact hU).of_isClosed_subset
  · exact (isClosed_closure.prod isClosed_singleton).union
      (isClosed_frontier.prod isClosed_Icc)
  · rintro z (hz | hz)
    · have ht : z.2 = 0 := hz.2
      refine ⟨hz.1, ?_⟩
      rw [ht]
      exact ⟨le_rfl, hT⟩
    · exact ⟨frontier_subset_closure hz.1, hz.2⟩

/-- A nonempty spatial domain supplies a point on the initial face, hence on
the exact parabolic boundary. -/
theorem parabolicBoundary_nonempty {n : Nat} {U : Set (Euclidean n)} {T : Real}
    (hU : U.Nonempty) (_hT : 0 ≤ T) : (parabolicBoundary U T).Nonempty := by
  obtain ⟨x, hx⟩ := hU
  exact ⟨(x, 0), Or.inl ⟨subset_closure hx, Set.mem_singleton 0⟩⟩

/-- Continuous functions attain a maximum on the frozen closed cylinder.
This realizes `M1188-L-ATTAIN` without weakening the witness conclusion. -/
theorem exists_closedCylinder_isMaxOn {n : Nat} {U : Set (Euclidean n)}
    {T : Real} {u : Euclidean n × Real → Real}
    (hU : U.Nonempty) (hbounded : Bornology.IsBounded U) (hT : 0 ≤ T)
    (hu : ContinuousOn u (closedCylinder U T)) :
    ∃ z ∈ closedCylinder U T, IsMaxOn u (closedCylinder U T) z := by
  exact (closedCylinder_isCompact hbounded).exists_isMaxOn
    (closedCylinder_nonempty hU hT) hu

/-- Continuous functions attain a maximum on the exact parabolic boundary. -/
theorem exists_parabolicBoundary_isMaxOn {n : Nat} {U : Set (Euclidean n)}
    {T : Real} {u : Euclidean n × Real → Real}
    (hU : U.Nonempty) (hbounded : Bornology.IsBounded U) (hT : 0 ≤ T)
    (hu : ContinuousOn u (closedCylinder U T)) :
    ∃ b ∈ parabolicBoundary U T, IsMaxOn u (parabolicBoundary U T) b := by
  have hcontinuous : ContinuousOn u (parabolicBoundary U T) := by
    apply hu.mono
    rintro z (hz | hz)
    · have ht : z.2 = 0 := hz.2
      refine ⟨hz.1, ?_⟩
      rw [ht]
      exact ⟨le_rfl, hT⟩
    · exact ⟨frontier_subset_closure hz.1, hz.2⟩
  exact (parabolicBoundary_isCompact hbounded hT).exists_isMaxOn
    (parabolicBoundary_nonempty hU hT) hcontinuous

/-- A point of `closure U` outside an open `U` lies on `frontier U`.  This is
the topology normalization needed by `M1188-N-BOUNDARY`. -/
theorem mem_frontier_of_mem_closure_not_mem {n : Nat} {U : Set (Euclidean n)}
    (hopen : IsOpen U) {x : Euclidean n} (hxclosure : x ∈ closure U)
    (hxU : x ∉ U) : x ∈ frontier U := by
  rw [frontier, hopen.interior_eq]
  exact ⟨hxclosure, hxU⟩

/-- A closed-cylinder point is on the parabolic boundary whenever its time is
zero or its spatial coordinate is not in the open domain. -/
theorem mem_parabolicBoundary_of_time_eq_zero_or_not_mem {n : Nat}
    {U : Set (Euclidean n)} {T : Real} (hopen : IsOpen U)
    {z : Euclidean n × Real} (hz : z ∈ closedCylinder U T)
    (hboundary : z.2 = 0 ∨ z.1 ∉ U) : z ∈ parabolicBoundary U T := by
  rcases hboundary with ht | hx
  · exact Or.inl ⟨hz.1, Set.mem_singleton_iff.mpr ht⟩
  · exact Or.inr ⟨mem_frontier_of_mem_closure_not_mem hopen hz.1 hx, hz.2⟩

/-- At a maximum over `[0, S]` attained at a positive time, the full time
derivative is nonnegative.  This includes the one-sided terminal case. -/
theorem deriv_nonneg_of_isMaxOn_Icc {f : Real → Real} {t S : Real}
    (ht : 0 < t) (htS : t ≤ S) (hf : DifferentiableAt Real f t)
    (hmax : IsMaxOn f (Icc 0 S) t) : 0 ≤ deriv f t := by
  have hdir : (0 : Real) - t ∈ posTangentConeAt (Icc 0 S) t := by
    apply sub_mem_posTangentConeAt_of_segment_subset
    rw [segment_symm, segment_eq_Icc ht.le]
    exact Icc_subset_Icc_right htS
  have h := hmax.localize.hasFDerivWithinAt_nonpos
    hf.hasFDerivAt.hasFDerivWithinAt hdir
  have hmul : 0 ≤ t * deriv f t := by simpa using h
  exact nonneg_of_mul_nonneg_right hmul ht

/-- The weak maximum principle in the local spelling used by this proof
module. -/
theorem weak_maximum_principle :
    ∀ (n : Nat), 1 ≤ n → ∀ (U : Set (Euclidean n)), U.Nonempty → IsOpen U →
    Bornology.IsBounded U → ∀ (T : Real), 0 < T →
      ∀ u : Euclidean n × Real → Real,
        Stage1Instances.THM_M_1188.HasClassicalHeatRegularity U T u →
        Stage1Instances.THM_M_1188.IsHeatSubsolution U T u →
          ∃ b ∈ parabolicBoundary U T, ∀ z ∈ closedCylinder U T, u z ≤ u b := by
  intro n _hn U hU hopen hbounded T hT u hregular hsub
  have hT0 : 0 ≤ T := hT.le
  have hboundaryCompact : IsCompact (parabolicBoundary U T) :=
    parabolicBoundary_isCompact hbounded hT0
  have hboundaryNonempty : (parabolicBoundary U T).Nonempty :=
    parabolicBoundary_nonempty hU hT0
  have huboundary : ContinuousOn u (parabolicBoundary U T) := by
    apply hregular.1.mono
    rintro z (hz | hz)
    · have ht : z.2 = 0 := hz.2
      refine ⟨hz.1, ?_⟩
      rw [ht]
      exact ⟨le_rfl, hT0⟩
    · exact ⟨frontier_subset_closure hz.1, hz.2⟩
  obtain ⟨b, hb, hbmax⟩ :=
    hboundaryCompact.exists_isMaxOn hboundaryNonempty huboundary
  refine ⟨b, hb, ?_⟩
  intro z hz
  apply le_of_forall_pos_le_add
  intro delta hdelta
  let eps : Real := delta / (T + 1)
  have hT1 : 0 < T + 1 := by linarith
  have heps : 0 < eps := div_pos hdelta hT1
  let w : Euclidean n × Real → Real := fun q ↦ u q - eps * q.2
  have hwcont : ContinuousOn w (closedCylinder U T) := by
    exact hregular.1.sub (continuous_const.mul continuous_snd).continuousOn
  have htruncated : ∀ (S : Real), 0 < S → S < T →
      ∀ q ∈ closedCylinder U S, w q ≤ u b := by
    intro S hS hST
    have huS : ContinuousOn u (closedCylinder U S) := by
      apply hregular.1.mono
      rintro q hq
      exact ⟨hq.1, hq.2.1, hq.2.2.trans hST.le⟩
    have hwS : ContinuousOn w (closedCylinder U S) := by
      exact huS.sub (continuous_const.mul continuous_snd).continuousOn
    obtain ⟨m, hm, hmmax⟩ :=
      exists_closedCylinder_isMaxOn hU hbounded hS.le hwS
    have hmboundary : m ∈ parabolicBoundary U S := by
      by_contra hmnot
      have hmU : m.1 ∈ U := by
        by_contra hmx
        exact hmnot (mem_parabolicBoundary_of_time_eq_zero_or_not_mem hopen hm
          (Or.inr hmx))
      have hmt_ne : m.2 ≠ 0 := by
        intro hmt
        exact hmnot (mem_parabolicBoundary_of_time_eq_zero_or_not_mem hopen hm
          (Or.inl hmt))
      have hmtpos : 0 < m.2 := lt_of_le_of_ne hm.2.1 (Ne.symm hmt_ne)
      have hmtT : m.2 < T := hm.2.2.trans_lt hST
      have hmtIocT : m.2 ∈ Ioc 0 T := ⟨hmtpos, hmtT.le⟩
      have hspaceMax : IsMaxOn (fun x : Euclidean n ↦ u (x, m.2)) U m.1 := by
        intro y hy
        have hwm : w (y, m.2) ≤ w m := hmmax ⟨subset_closure hy, hm.2⟩
        change u (y, m.2) - eps * m.2 ≤
          u (m.1, m.2) - eps * m.2 at hwm
        exact sub_le_sub_iff_right (eps * m.2) |>.mp hwm
      have hspaceLocal : IsLocalMax (fun x : Euclidean n ↦ u (x, m.2)) m.1 :=
        hspaceMax.isLocalMax (hopen.mem_nhds hmU)
      have hspaceCD : ContDiffAt Real 2 (fun x : Euclidean n ↦ u (x, m.2)) m.1 :=
        ((hregular.2.1 m.2 hmtIocT) m.1 hmU).contDiffAt
          (hopen.mem_nhds hmU)
      have hlap : Laplacian.laplacian (fun x : Euclidean n ↦ u (x, m.2)) m.1 ≤ 0 :=
        laplacian_nonpos_of_isLocalMax hspaceLocal hspaceCD
      have htimeCD : ContDiffAt Real 1 (fun t : Real ↦ u (m.1, t)) m.2 :=
        ((hregular.2.2 m.1 hmU) m.2 hmtIocT).contDiffAt
          (Ioc_mem_nhds hmtpos hmtT)
      have htimeDiff : DifferentiableAt Real (fun t : Real ↦ u (m.1, t)) m.2 :=
        htimeCD.differentiableAt (by norm_num)
      have hwtimeDiff : DifferentiableAt Real
          (fun t : Real ↦ u (m.1, t) - eps * t) m.2 :=
        htimeDiff.sub (by fun_prop)
      have htimeMax : IsMaxOn (fun t : Real ↦ u (m.1, t) - eps * t)
          (Icc 0 S) m.2 := by
        intro t ht
        exact hmmax ⟨hm.1, ht⟩
      have htimeNonneg : 0 ≤
          deriv (fun t : Real ↦ u (m.1, t) - eps * t) m.2 :=
        deriv_nonneg_of_isMaxOn_Icc hmtpos hm.2.2 hwtimeDiff htimeMax
      have hderivEq : deriv (fun t : Real ↦ u (m.1, t) - eps * t) m.2 =
          deriv (fun t : Real ↦ u (m.1, t)) m.2 - eps := by
        change deriv ((fun t : Real ↦ u (m.1, t)) -
          (fun t : Real ↦ eps * t)) m.2 = _
        rw [deriv_sub htimeDiff (by fun_prop)]
        rw [(hasDerivAt_const_mul (x := m.2) eps).deriv]
      rw [hderivEq] at htimeNonneg
      have hheat := hsub m.1 hmU m.2 hmtIocT
      exact (not_lt_of_ge htimeNonneg) (by
        have : deriv (fun t : Real ↦ u (m.1, t)) m.2 < eps := by
          linarith
        linarith)
    intro q hq
    have hqmax : w q ≤ w m := hmmax hq
    have hmfull : m ∈ parabolicBoundary U T := by
      rcases hmboundary with hm0 | hmlateral
      · exact Or.inl hm0
      · exact Or.inr ⟨hmlateral.1,
          hmlateral.2.1, hmlateral.2.2.trans hST.le⟩
    have hum : u m ≤ u b := hbmax hmfull
    dsimp [w] at hqmax ⊢
    have hmt0 : 0 ≤ m.2 := hm.2.1
    nlinarith
  have hbase : ∀ q ∈ closure U ×ˢ Ico 0 T, w q ≤ u b := by
    intro q hq
    by_cases hqt : q.2 = 0
    · have hqboundary : q ∈ parabolicBoundary U T := Or.inl ⟨hq.1, hqt⟩
      have := hbmax hqboundary
      dsimp [w]
      rw [hqt]
      simpa using this
    · have hqtpos : 0 < q.2 := lt_of_le_of_ne hq.2.1 (Ne.symm hqt)
      let S : Real := (q.2 + T) / 2
      have hS : 0 < S := by dsimp [S]; linarith
      have hST : S < T := by dsimp [S]; linarith [hq.2.2]
      have hqtS : q.2 ≤ S := by dsimp [S]; linarith [hq.2.2]
      exact htruncated S hS hST q ⟨hq.1, hq.2.1, hqtS⟩
  have hclosure : closure (closure U ×ˢ Ico 0 T) = closedCylinder U T := by
    rw [closure_prod_eq, isClosed_closure.closure_eq,
      closure_Ico (show (0 : Real) ≠ T from hT.ne)]
    rfl
  have hwle : w z ≤ u b := by
    rw [← hclosure] at hz hwcont
    exact le_on_closure hbase hwcont continuousOn_const hz
  dsimp [w, eps] at hwle
  have hztime : 0 ≤ z.2 ∧ z.2 ≤ T := hz.2
  have hepszt : delta / (T + 1) * z.2 ≤ delta := by
    have hratio : z.2 / (T + 1) ≤ 1 := by
      apply (div_le_one hT1).2
      linarith
    rw [div_mul_eq_mul_div]
    calc
      delta * z.2 / (T + 1) = delta * (z.2 / (T + 1)) := by ring
      _ ≤ delta * 1 := mul_le_mul_of_nonneg_left hratio hdelta.le
      _ = delta := mul_one delta
  linarith

/-- Exact canonical root, with no theorem broadening or substituted boundary. -/
theorem heatEquationWeakMaximumPrinciple :
    Stage1Instances.THM_M_1188.HeatEquationWeakMaximumPrincipleTarget := by
  simpa only [Stage1Instances.THM_M_1188.HeatEquationWeakMaximumPrincipleTarget,
    Stage1Instances.THM_M_1188.closedCylinder,
    Stage1Instances.THM_M_1188.parabolicBoundary] using weak_maximum_principle

/-- The proved analytic body inhabits the terminal interface frozen before
proof execution. -/
theorem analyticMaximumEngine :
    Stage1Instances.THM_M_1188.ObligationTree.AnalyticMaximumEngine := by
  simpa only [Stage1Instances.THM_M_1188.ObligationTree.AnalyticMaximumEngine,
    Stage1Instances.THM_M_1188.ObligationTree.BoundaryDominance,
    Stage1Instances.THM_M_1188.ObligationTree.HasClassicalHeatRegularity,
    Stage1Instances.THM_M_1188.ObligationTree.IsHeatSubsolution,
    Stage1Instances.THM_M_1188.ObligationTree.closedCylinder,
    Stage1Instances.THM_M_1188.ObligationTree.parabolicBoundary] using
      weak_maximum_principle

/-- Exact child-to-root replay through the frozen obligation-tree composer. -/
theorem assembledObligationRoot :
    Stage1Instances.THM_M_1188.ObligationTree.Root :=
  Stage1Instances.THM_M_1188.ObligationTree.root_compose analyticMaximumEngine

#print axioms closedCylinder_isCompact
#print axioms iteratedDeriv_two_nonpos_of_isLocalMax
#print axioms directional_second_eq
#print axioms laplacian_nonpos_of_isLocalMax
#print axioms closedCylinder_nonempty
#print axioms parabolicBoundary_isCompact
#print axioms parabolicBoundary_nonempty
#print axioms exists_closedCylinder_isMaxOn
#print axioms exists_parabolicBoundary_isMaxOn
#print axioms mem_frontier_of_mem_closure_not_mem
#print axioms mem_parabolicBoundary_of_time_eq_zero_or_not_mem
#print axioms deriv_nonneg_of_isMaxOn_Icc
#print axioms weak_maximum_principle
#print axioms heatEquationWeakMaximumPrinciple
#print axioms analyticMaximumEngine
#print axioms assembledObligationRoot

end Stage1Instances.THM_M_1188.Proof
