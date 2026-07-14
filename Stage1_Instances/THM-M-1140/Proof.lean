import ObligationTree
import Mathlib.Analysis.Calculus.DerivativeTest
import Mathlib.Analysis.InnerProductSpace.Calculus
import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Analysis.InnerProductSpace.Harmonic.HarmonicContOnCl
import Mathlib.Topology.Connected.Clopen
import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import Mathlib.Analysis.Normed.Affine.AddTorsor

open Set Topology Filter
open InnerProductSpace

namespace Barrier

theorem isLocalMax_iteratedDeriv_two_nonpos {f : Real -> Real} {x : Real}
    (hf : ContDiffAt Real 2 f x) (hmax : IsLocalMax f x) :
    iteratedDeriv 2 f x <= 0 := by
  rw [show iteratedDeriv 2 f = deriv (deriv f) by
    simpa [iteratedDeriv_succ] using iteratedDeriv_succ (n := 1) f]
  apply le_of_not_gt
  intro hpos
  have hmin : IsLocalMin f x :=
    isLocalMin_of_deriv_deriv_pos hpos hmax.deriv_eq_zero hf.continuousAt
  have heq : f =ᶠ[nhds x] fun _ => f x :=
    eventuallyEq_of_isMinFilter_of_isMaxFilter hmin hmax
  have hderiv : deriv f =ᶠ[nhds x] fun _ => 0 := by
    simpa using heq.deriv
  have hzero : deriv (deriv f) x = 0 := by
    rw [hderiv.deriv_eq]
    exact deriv_const _ _
  exact hpos.ne' hzero

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace Real E]
  [FiniteDimensional Real E]

theorem isLocalMax_iteratedFDeriv_two_apply_nonpos {f : E -> Real} {x e : E}
    (hf : ContDiffAt Real 2 f x) (hmax : IsLocalMax f x) :
    iteratedFDeriv Real 2 f x ![e, e] <= 0 := by
  let F : E -> Real := fun z => f (z + x)
  let L : Real →L[Real] E := ContinuousLinearMap.toSpanSingleton Real e
  have hF : ContDiffAt Real 2 F 0 := by
    apply (show ContDiffAt Real 2 f (0 + x) by simpa using hf).comp 0
    fun_prop
  have hFL : ContDiffAt Real 2 (F ∘ L) 0 := by
    have hF0 : ContDiffAt Real 2 F (L 0) := by simpa using hF
    exact hF0.comp 0 L.contDiff.contDiffAt
  have hmaxF : IsLocalMax F 0 := by
    have hmax0 : IsLocalMax f (0 + x) := by simpa using hmax
    have h := hmax0.comp_continuous (g := fun z : E => z + x) (b := 0) (by fun_prop)
    simpa [F, Function.comp_def] using h
  have hmaxFL : IsLocalMax (F ∘ L) 0 := by
    have hmax0 : IsLocalMax F (L 0) := by simpa using hmaxF
    exact hmax0.comp_continuous (g := L) (b := 0) L.continuous.continuousAt
  have hnonpos := isLocalMax_iteratedDeriv_two_nonpos hFL hmaxFL
  rw [iteratedDeriv_eq_iteratedFDeriv] at hnonpos
  have hcomp :
      iteratedFDeriv Real 2 (F ∘ L) 0 =
        (iteratedFDeriv Real 2 F 0).compContinuousLinearMap fun _ => L := by
    rcases hF.contDiffOn (m := 2) le_rfl (by simp) with ⟨s, hs, hFs⟩
    rcases mem_nhds_iff.mp hs with ⟨t, hts, htopen, h0t⟩
    have hFt : ContDiffOn Real 2 F t := hFs.mono hts
    have hpreopen : IsOpen (L ⁻¹' t) := htopen.preimage L.continuous
    have h0pre : (0 : Real) ∈ L ⁻¹' t := by simpa [L] using h0t
    calc
      iteratedFDeriv Real 2 (F ∘ L) 0 =
          iteratedFDerivWithin Real 2 (F ∘ L) (L ⁻¹' t) 0 :=
        (iteratedFDerivWithin_eq_iteratedFDeriv hpreopen.uniqueDiffOn hFL h0pre).symm
      _ = (iteratedFDerivWithin Real 2 F t (L 0)).compContinuousLinearMap fun _ => L :=
        L.iteratedFDerivWithin_comp_right hFt htopen.uniqueDiffOn hpreopen.uniqueDiffOn
          h0pre le_rfl
      _ = (iteratedFDeriv Real 2 F 0).compContinuousLinearMap fun _ => L := by
        rw [show L 0 = 0 by simp]
        rw [iteratedFDerivWithin_eq_iteratedFDeriv htopen.uniqueDiffOn hF h0t]
  change ((iteratedFDeriv Real 2 (F ∘ L) 0) fun _ => (1 : Real)) <= 0 at hnonpos
  rw [hcomp] at hnonpos
  rw [show iteratedFDeriv Real 2 F 0 = iteratedFDeriv Real 2 f x by
    simpa [F] using iteratedFDeriv_comp_add_right (𝕜 := Real) (f := f) 2 x 0] at hnonpos
  have hv : ![e, e] = (fun _ : Fin 2 => e) := by
    funext i
    fin_cases i <;> rfl
  rw [hv]
  convert hnonpos using 1 <;>
    simp [L, ContinuousMultilinearMap.compContinuousLinearMap_apply]

theorem isLocalMax_laplacian_nonpos {f : E -> Real} {x : E}
    (hf : ContDiffAt Real 2 f x) (hmax : IsLocalMax f x) :
    Laplacian.laplacian f x <= 0 := by
  rw [InnerProductSpace.laplacian_eq_iteratedFDeriv_stdOrthonormalBasis]
  exact Finset.sum_nonpos fun i _ =>
    isLocalMax_iteratedFDeriv_two_apply_nonpos hf hmax

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace Real E]
  [FiniteDimensional Real E]

/- The exponential radial function from which the Gaussian barrier is built. -/
noncomputable def radialExpBarrier (center : E) (alpha : Real) : E -> Real :=
  fun x => Real.exp (alpha * dist x center ^ 2)

theorem radialExpBarrier_contDiff (center : E) (alpha : Real) :
    ContDiff Real 2 (radialExpBarrier center alpha) := by
  have hsq : ContDiff Real 2 (fun x : E => dist x center ^ 2) := by
    simpa [dist_eq_norm] using
      (contDiff_norm_sq Real).comp (contDiff_id.sub contDiff_const)
  simpa [radialExpBarrier] using (ContDiff.const_smul alpha hsq).exp

theorem fderiv_radialExpBarrier (center : E) (alpha : Real) (x : E) :
    fderiv Real (radialExpBarrier center alpha) x =
      (2 * alpha * radialExpBarrier center alpha x) •
        innerSL Real (x - center) := by
  have hdiffsq : DifferentiableAt Real (fun z : E => dist z center ^ 2) x := by
    have hsq : ContDiff Real 2 (fun z : E => dist z center ^ 2) := by
      simpa [dist_eq_norm] using
        (contDiff_norm_sq Real).comp (contDiff_id.sub contDiff_const)
    exact hsq.contDiffAt.differentiableAt (by norm_num)
  rw [show radialExpBarrier center alpha =
      fun z : E => Real.exp (alpha * dist z center ^ 2) by rfl]
  rw [fderiv_exp (hdiffsq.const_mul alpha)]
  have hshift : fderiv Real (fun z : E => dist z center ^ 2) x =
      2 • innerSL Real (x - center) := by
    simpa [dist_eq_norm] using
      ((hasStrictFDerivAt_norm_sq (x - center)).comp x
        ((hasStrictFDerivAt_id x).sub_const center)).hasFDerivAt.fderiv
  rw [fderiv_const_mul hdiffsq alpha, hshift]
  ext v
  simp [radialExpBarrier]
  ring

theorem fderiv_innerSL_sub (center : E) (x : E) :
    fderiv Real (fun z : E => innerSL Real (z - center)) x =
      (innerSL Real (E := E)).toContinuousLinearMap := by
  have hinner : HasFDerivAt (innerSL Real (E := E))
      (innerSL Real (E := E)).toContinuousLinearMap (x - center) :=
    (innerSL Real (E := E)).toContinuousLinearMap.hasFDerivAt
  have h := (hinner.comp x ((hasFDerivAt_id x).sub_const center)).fderiv
  simpa only [Function.comp_apply] using h

theorem fderiv_fderiv_radialExpBarrier (center : E) (alpha : Real) (x : E) :
    fderiv Real (fun z => fderiv Real (radialExpBarrier center alpha) z) x =
      (2 * alpha * radialExpBarrier center alpha x) •
          (innerSL Real (E := E)).toContinuousLinearMap +
        ((2 * alpha) • fderiv Real (radialExpBarrier center alpha) x).smulRight
          (innerSL Real (x - center)) := by
  have hEq : (fun z => fderiv Real (radialExpBarrier center alpha) z) =
      fun z => (2 * alpha * radialExpBarrier center alpha z) •
        innerSL Real (z - center) := by
    funext z
    exact fderiv_radialExpBarrier center alpha z
  rw [hEq]
  have hc : DifferentiableAt Real
      (fun z : E => 2 * alpha * radialExpBarrier center alpha z) x := by
    have hcd : ContDiff Real 2 (radialExpBarrier center alpha) :=
      radialExpBarrier_contDiff center alpha
    exact (hcd.contDiffAt.differentiableAt (by norm_num)).const_mul (2 * alpha)
  have hf : DifferentiableAt Real (fun z : E => innerSL Real (z - center)) x := by
    exact (innerSL Real (E := E)).toContinuousLinearMap.differentiableAt.comp x
      ((differentiableAt_id.sub_const center))
  rw [fderiv_fun_smul hc hf]
  rw [fderiv_innerSL_sub]
  have hcd : ContDiff Real 2 (radialExpBarrier center alpha) :=
    radialExpBarrier_contDiff center alpha
  rw [fderiv_const_mul (hcd.contDiffAt.differentiableAt (by norm_num)) (2 * alpha)]

theorem laplacian_radialExpBarrier (center : E) (alpha : Real) (x : E) :
    Laplacian.laplacian (radialExpBarrier center alpha) x =
      (2 * alpha * (Module.finrank Real E : Real) +
        4 * alpha ^ 2 * dist x center ^ 2) *
        radialExpBarrier center alpha x := by
  rw [InnerProductSpace.laplacian_eq_iteratedFDeriv_stdOrthonormalBasis]
  have hsecond := fderiv_fderiv_radialExpBarrier center alpha x
  have hdir (i : Fin (Module.finrank Real E)) :
      fderiv Real (fderiv Real (radialExpBarrier center alpha)) x
          ((stdOrthonormalBasis Real E) i) ((stdOrthonormalBasis Real E) i) =
        2 * alpha * radialExpBarrier center alpha x +
          4 * alpha ^ 2 * radialExpBarrier center alpha x *
            (inner Real (x - center) ((stdOrthonormalBasis Real E) i)) ^ 2 := by
    rw [hsecond]
    simp only [ContinuousLinearMap.add_apply, ContinuousLinearMap.coe_smul', Pi.smul_apply,
      ContinuousLinearMap.smulRight_apply, innerSL_apply_apply]
    rw [fderiv_radialExpBarrier]
    simp only [ContinuousLinearMap.coe_smul', Pi.smul_apply, innerSL_apply_apply]
    change (2 * alpha * radialExpBarrier center alpha x) *
        inner Real ((stdOrthonormalBasis Real E) i) ((stdOrthonormalBasis Real E) i) + _ = _
    rw [show inner Real ((stdOrthonormalBasis Real E) i)
        ((stdOrthonormalBasis Real E) i) = 1 by simp]
    rw [real_inner_comm ((stdOrthonormalBasis Real E) i) (x - center)]
    simp only [smul_eq_mul]
    ring
  simp only [iteratedFDeriv_two_apply, Matrix.cons_val_zero, Matrix.cons_val_one,
    Matrix.cons_val_fin_one]
  rw [Finset.sum_congr rfl (fun i _ => hdir i)]
  rw [Finset.sum_add_distrib]
  rw [← Finset.mul_sum]
  rw [← Finset.mul_sum]
  simp only [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul]
  rw [(stdOrthonormalBasis Real E).sum_sq_inner_left]
  rw [dist_eq_norm]
  ring

noncomputable def gaussian (a : E) (alpha : Real) : E -> Real :=
  radialExpBarrier a (-alpha)

theorem gaussian_contDiff (a : E) (alpha : Real) :
    ContDiff Real 2 (gaussian a alpha) := by
  simpa [gaussian] using radialExpBarrier_contDiff a (-alpha)

theorem fderiv_gaussian_apply (a x e : E) (alpha : Real) :
    fderiv Real (gaussian a alpha) x e =
      (-2 * alpha * Real.exp (-alpha * ‖x - a‖ ^ 2)) * ⟪x - a, e⟫_Real := by
  rw [show gaussian a alpha = radialExpBarrier a (-alpha) by rfl]
  rw [fderiv_radialExpBarrier]
  simp only [radialExpBarrier, neg_mul, dist_eq_norm, ContinuousLinearMap.smul_apply,
    innerSL_apply_apply]
  simp only [smul_eq_mul]
  ring

theorem laplacian_gaussian (a x : E) (alpha : Real) :
    Laplacian.laplacian (gaussian a alpha) x =
      Real.exp (-alpha * ‖x - a‖ ^ 2) *
        (4 * alpha ^ 2 * ‖x - a‖ ^ 2 -
          2 * alpha * Module.finrank Real E) := by
  rw [show gaussian a alpha = radialExpBarrier a (-alpha) by rfl]
  rw [laplacian_radialExpBarrier]
  simp [radialExpBarrier, dist_eq_norm]
  ring

theorem laplacian_gaussian_pos_of (a x : E) (alpha : Real)
    (ha : 0 < alpha)
    (hr : (Module.finrank Real E : Real) < 2 * alpha * ‖x - a‖ ^ 2) :
    0 < Laplacian.laplacian (gaussian a alpha) x := by
  rw [laplacian_gaussian]
  have hexp : 0 < Real.exp (-alpha * ‖x - a‖ ^ 2) := Real.exp_pos _
  have hfactor : 0 < 4 * alpha ^ 2 * ‖x - a‖ ^ 2 -
      2 * alpha * Module.finrank Real E := by
    nlinarith
  positivity

/- A strictly subharmonic function cannot realize a maximum at an interior
point of a set on which it is C2. -/
theorem strictSubharmonic_max_mem_frontier {K : Set E} {v : E -> Real} {z : E}
    (hKclosed : IsClosed K) (hzK : z ∈ K)
    (hv : ContDiffAt Real 2 v z)
    (hlap : 0 < Laplacian.laplacian v z)
    (hzmax : IsMaxOn v K z) : z ∈ frontier K := by
  have hznotint : z ∉ interior K := by
    intro hzint
    have hzlocal : IsLocalMax v z := hzmax.isLocalMax (mem_interior_iff_mem_nhds.mp hzint)
    have hnonpos := isLocalMax_laplacian_nonpos hv hzlocal
    linarith
  rw [hKclosed.frontier_eq]
  exact ⟨hzK, hznotint⟩

theorem strictSubharmonic_le_of_boundary_le
    {K : Set E} {v : E -> Real} {C : Real}
    (hKcompact : IsCompact K) (hKne : K.Nonempty)
    (hvcont : ContinuousOn v K)
    (hvC2 : ∀ z ∈ interior K, ContDiffAt Real 2 v z)
    (hlap : ∀ z ∈ interior K, 0 < Laplacian.laplacian v z)
    (hfrontier : ∀ z ∈ frontier K, v z ≤ C) :
    ∀ z ∈ K, v z ≤ C := by
  obtain ⟨w, hwK, hwmax⟩ := hKcompact.exists_isMaxOn hKne hvcont
  by_cases hwint : w ∈ interior K
  · have hwlocal : IsLocalMax v w :=
      hwmax.isLocalMax (mem_interior_iff_mem_nhds.mp hwint)
    have hnonpos := isLocalMax_laplacian_nonpos (hvC2 w hwint) hwlocal
    exact (not_lt_of_ge hnonpos (hlap w hwint)).elim
  have hwfront : w ∈ frontier K := by
    rw [hKcompact.isClosed.frontier_eq]
    exact ⟨hwK, hwint⟩
  intro z hz
  exact (hwmax hz).trans (hfrontier w hwfront)


/- The compact inner cap has a uniform gap below the tangent value. -/
theorem innerBall_uniform_gap
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace Real E]
      [FiniteDimensional Real E]
    {u : E -> Real} {x b : E} {R : Real}
    (hR : 0 < R) (hucont : ContinuousOn u (Metric.closedBall x (R / 2)))
    (hballlt : ∀ z ∈ Metric.ball x R, u z < u b) :
    ∃ m : Real, m < u b ∧ ∀ z ∈ Metric.closedBall x (R / 2), u z ≤ m := by
  have hhalf : 0 < R / 2 := by positivity
  have hne : (Metric.closedBall x (R / 2)).Nonempty :=
    ⟨x, Metric.mem_closedBall_self hhalf.le⟩
  obtain ⟨w, hw, hwmax⟩ :=
    (isCompact_closedBall x (R / 2)).exists_isMaxOn
      hne hucont
  refine ⟨u w, ?_, fun z hz => hwmax hz⟩
  apply hballlt w
  exact Metric.closedBall_subset_ball (by linarith) hw


noncomputable def annulus (x : E) (R : Real) : Set E :=
  Metric.closedBall x R ∩ (Metric.ball x (R / 2))ᶜ

theorem annulus_compact (x : E) (R : Real) : IsCompact (annulus x R) := by
  exact (isCompact_closedBall x R).inter_right Metric.isOpen_ball.isClosed_compl

theorem mem_annulus_iff {x z : E} {R : Real} :
    z ∈ annulus x R ↔ R / 2 ≤ dist z x ∧ dist z x ≤ R := by
  simp only [annulus, mem_inter_iff, Metric.mem_closedBall, mem_compl_iff,
    Metric.mem_ball, not_lt]
  tauto

theorem annulus_nonempty {x : E} {R : Real} (hR : 0 < R)
    [Nontrivial E] : (annulus x R).Nonempty := by
  obtain ⟨e : E, he⟩ := exists_norm_eq E hR.le
  refine ⟨x + e, mem_annulus_iff.mpr ?_⟩
  simp [dist_eq_norm, he]
  linarith

theorem frontier_annulus_subset {x : E} {R : Real} (hR : 0 < R) :
    frontier (annulus x R) ⊆ Metric.sphere x R ∪ Metric.sphere x (R / 2) := by
  intro z hz
  have hz' := frontier_inter_subset (Metric.closedBall x R) (Metric.ball x (R / 2))ᶜ hz
  rcases hz' with hzout | hzin
  · exact Or.inl (Metric.frontier_closedBall_subset_sphere hzout.1)
  · exact Or.inr (by
      rw [frontier_compl] at hzin
      exact Metric.frontier_ball_subset_sphere hzin.2)


noncomputable def barrierFunction (u : E -> Real) (a : E) (R alpha eps : Real) : E -> Real :=
  fun z => u z + eps * (gaussian a alpha z - Real.exp (-alpha * R ^ 2))

theorem barrierFunction_contDiffAt {u : E -> Real} {a z : E} {R alpha eps : Real}
    (hu : ContDiffAt Real 2 u z) :
    ContDiffAt Real 2 (barrierFunction u a R alpha eps) z := by
  exact hu.add (ContDiffAt.const_smul eps
    ((gaussian_contDiff a alpha).contDiffAt.sub contDiffAt_const))

theorem laplacian_barrierFunction {u : E -> Real} {a z : E} {R alpha eps : Real}
    (hu : ContDiffAt Real 2 u z) :
    Laplacian.laplacian (barrierFunction u a R alpha eps) z =
      Laplacian.laplacian u z + eps * Laplacian.laplacian (gaussian a alpha) z := by
  let q : E -> Real := fun w => eps * (gaussian a alpha w - Real.exp (-alpha * R ^ 2))
  have hq : ContDiffAt Real 2 q z := by
    unfold q
    exact contDiffAt_const.mul
      ((gaussian_contDiff a alpha).contDiffAt.sub contDiffAt_const)
  have hqeq : q = eps • (gaussian a alpha - fun _ => Real.exp (-alpha * R ^ 2)) := by
    ext w
    simp [q, Pi.sub_apply]
  unfold barrierFunction
  change Laplacian.laplacian (u + q) z = _
  rw [hu.laplacian_add hq]
  rw [hqeq, InnerProductSpace.laplacian_smul eps]
  · have hc : ContDiffAt Real 2
        (fun _ : E => Real.exp (-alpha * R ^ 2)) z := contDiffAt_const
    rw [(gaussian_contDiff a alpha).contDiffAt.laplacian_sub hc]
    simp
  · have hc : ContDiffAt Real 2
        (fun _ : E => Real.exp (-alpha * R ^ 2)) z := contDiffAt_const
    exact (gaussian_contDiff a alpha).contDiffAt.sub hc


theorem gaussian_le_inner_on_annulus {a z : E} {R alpha : Real}
    (hR : 0 < R) (ha : 0 < alpha) (hz : z ∈ annulus a R) :
    gaussian a alpha z - Real.exp (-alpha * R ^ 2) ≤
      Real.exp (-alpha * (R / 2) ^ 2) - Real.exp (-alpha * R ^ 2) := by
  have hdist := (mem_annulus_iff.mp hz).1
  have hsq : (R / 2) ^ 2 ≤ ‖z - a‖ ^ 2 := by
    rw [← dist_eq_norm]
    nlinarith [dist_nonneg (x := z) (y := a)]
  have harg : -alpha * ‖z - a‖ ^ 2 ≤ -alpha * (R / 2) ^ 2 := by
    nlinarith
  rw [show gaussian a alpha z = Real.exp (-alpha * ‖z - a‖ ^ 2) by
    simp [gaussian, radialExpBarrier, dist_eq_norm]]
  exact sub_le_sub_right (Real.exp_le_exp.mpr harg) _

theorem gaussian_eq_zero_barrier_on_outer {a z : E} {R alpha : Real}
    (hz : z ∈ Metric.sphere a R) :
    gaussian a alpha z - Real.exp (-alpha * R ^ 2) = 0 := by
  rw [Metric.mem_sphere, dist_eq_norm] at hz
  rw [show gaussian a alpha z = Real.exp (-alpha * ‖z - a‖ ^ 2) by
    simp [gaussian, radialExpBarrier, dist_eq_norm]]
  rw [hz]
  ring

theorem gaussian_barrier_pos_on_inner {R alpha : Real}
    (hR : 0 < R) (ha : 0 < alpha) :
    0 < Real.exp (-alpha * (R / 2) ^ 2) - Real.exp (-alpha * R ^ 2) := by
  apply sub_pos.mpr
  apply Real.exp_lt_exp.mpr
  have hsq : (R / 2) ^ 2 < R ^ 2 := by nlinarith
  nlinarith


/- Comparison on the annulus for a small positive Gaussian perturbation. -/
theorem gaussian_annulus_comparison
    {Omega : Set E} {u : E -> Real} {a b : E} {R m alpha eps : Real}
    (hR : 0 < R) (hab : dist a b = R)
    (hdim : 0 < Module.finrank Real E)
    (hclosedOmega : Metric.closedBall a R ⊆ Omega)
    (hharm : InnerProductSpace.HarmonicOnNhd u Omega)
    (hmax : ∀ z ∈ Omega, u z ≤ u b)
    (hub : u b = u b)
    (hum : m < u b)
    (hinner : ∀ z ∈ Metric.closedBall a (R / 2), u z ≤ m)
    (ha : 0 < alpha)
    (halarge : (Module.finrank Real E : Real) < 2 * alpha * (R / 2) ^ 2)
    (heps : 0 < eps)
    (hepssmall : eps *
        (Real.exp (-alpha * (R / 2) ^ 2) - Real.exp (-alpha * R ^ 2)) ≤ u b - m) :
    ∀ z ∈ annulus a R, barrierFunction u a R alpha eps z ≤ u b := by
  let K := annulus a R
  have hKcompact : IsCompact K := annulus_compact a R
  haveI : Nontrivial E := Module.nontrivial_of_finrank_pos hdim
  have hKne : K.Nonempty := annulus_nonempty hR
  have hvcont : ContinuousOn (barrierFunction u a R alpha eps) K := by
    intro z hz
    exact (barrierFunction_contDiffAt
      (hharm z (hclosedOmega hz.1)).1).continuousAt.continuousWithinAt
  apply strictSubharmonic_le_of_boundary_le hKcompact hKne hvcont
  · intro z hz
    have hzK : z ∈ K := interior_subset hz
    exact barrierFunction_contDiffAt (hharm z (hclosedOmega hzK.1)).1
  · intro z hz
    have hzK : z ∈ K := interior_subset hz
    have hzlower : R / 2 < dist z a := by
      have hzint : z ∈ interior (Metric.ball a (R / 2))ᶜ := by
        change z ∈ interior (Metric.closedBall a R ∩ (Metric.ball a (R / 2))ᶜ) at hz
        rw [interior_inter] at hz
        exact hz.2
      have : z ∈ (Metric.closedBall a (R / 2))ᶜ := by
        rw [interior_compl, closure_ball a (by linarith)] at hzint
        exact hzint
      simpa [Metric.mem_closedBall, not_le] using this
    have hrank : (Module.finrank Real E : Real) < 2 * alpha * ‖z - a‖ ^ 2 := by
      rw [← dist_eq_norm]
      have hsquares : (R / 2) ^ 2 < dist z a ^ 2 := by
        nlinarith [dist_nonneg (x := z) (y := a)]
      nlinarith
    rw [laplacian_barrierFunction (hharm z (hclosedOmega hzK.1)).1]
    have hulap : Laplacian.laplacian u z = 0 :=
      (hharm z (hclosedOmega hzK.1)).2.self_of_nhds
    rw [hulap, zero_add]
    exact mul_pos heps (laplacian_gaussian_pos_of a z alpha ha hrank)
  · intro z hzfront
    rcases frontier_annulus_subset hR hzfront with hzouter | hzinner
    · unfold barrierFunction
      rw [gaussian_eq_zero_barrier_on_outer hzouter, mul_zero, add_zero]
      apply hmax z
      apply hclosedOmega
      exact Metric.mem_closedBall.mpr (Metric.mem_sphere.mp hzouter).le
    · unfold barrierFunction
      have hzclosed : z ∈ Metric.closedBall a (R / 2) := by
        exact Metric.mem_closedBall.mpr (Metric.mem_sphere.mp hzinner).le
      calc
        u z + eps * (gaussian a alpha z - Real.exp (-alpha * R ^ 2))
            ≤ m + eps * (Real.exp (-alpha * (R / 2) ^ 2) -
                Real.exp (-alpha * R ^ 2)) := by
              gcongr
              · exact hinner z hzclosed
              · have hg := gaussian_le_inner_on_annulus hR ha
                    (hKcompact.isClosed.closure_eq ▸ frontier_subset_closure hzfront)
                linarith
        _ ≤ u b := by linarith


/- A positive inward derivative contradicts comparison on the tangent annulus. -/
theorem tangentBarrier_derivative_contradiction
    {Omega : Set E} {u : E -> Real} {a b : E} {R alpha eps : Real}
    (hOmega : IsOpen Omega) (hbOmega : b ∈ Omega)
    (huC2 : ContDiffAt Real 2 u b)
    (hmax : ∀ z ∈ Omega, u z ≤ u b)
    (hR : 0 < R) (hab : dist a b = R)
    (ha : 0 < alpha) (heps : 0 < eps)
    (hcomp : ∀ z ∈ annulus a R,
      barrierFunction u a R alpha eps z ≤ u b) : False := by
  let v := barrierFunction u a R alpha eps
  let e : Real → E := AffineMap.lineMap b a
  let phi : Real → Real := v ∘ e
  have hbmax : IsLocalMax u b := by
    have hbmaxOn : IsMaxOn u Omega b := fun z hz => hmax z hz
    exact hbmaxOn.isLocalMax (hOmega.mem_nhds hbOmega)
  have hufderiv : fderiv Real u b = 0 := hbmax.fderiv_eq_zero
  have hvderiv : HasFDerivAt v
      (fderiv Real v b) b :=
    ((barrierFunction_contDiffAt huC2).differentiableAt (by norm_num)).hasFDerivAt
  have hphideriv : HasDerivAt phi (fderiv Real v b (a - b)) 0 := by
    simpa only [phi, e, AffineMap.lineMap_apply_zero] using
      hvderiv.comp_hasDerivAt_of_eq (x := (0 : Real))
        (AffineMap.hasDerivAt_lineMap (a := b) (b := a) (x := (0 : Real)))
        (by simp)
  have hline : ∀ t ∈ Set.Ioo (0 : Real) (1 / 2), e t ∈ annulus a R := by
    intro t ht
    apply mem_annulus_iff.mpr
    have hdist : dist (e t) a = (1 - t) * R := by
      change dist (AffineMap.lineMap b a t) a = _
      rw [dist_lineMap_right, Real.norm_eq_abs,
        abs_of_pos (show 0 < 1 - t by have := ht.2; linarith)]
      rw [show dist b a = R by simpa [dist_comm] using hab]
    rw [hdist]
    constructor
    · nlinarith [mul_nonneg hR.le (sub_nonneg.mpr ht.2.le)]
    · nlinarith [mul_nonneg hR.le ht.1.le]
  have hnorm : ‖b - a‖ = R := by
    rw [← dist_eq_norm, dist_comm]
    exact hab
  have hvb : v b = u b := by
    dsimp [v, barrierFunction, gaussian, radialExpBarrier]
    rw [show dist b a = R by simpa [dist_comm] using hab]
    simp
  have hphi0 : phi 0 = u b := by
    simpa [phi, e] using hvb
  have hslope_nonpos : ∀ᶠ t in 𝓝[>] (0 : Real),
      t⁻¹ • (phi (0 + t) - phi 0) ≤ 0 := by
    filter_upwards [Ioo_mem_nhdsGT (show (0 : Real) < 1 / 2 by norm_num)] with t ht
    have hvt : v (e t) ≤ u b := hcomp _ (hline t ht)
    have hdiff : phi (0 + t) - phi 0 ≤ 0 := by
      rw [hphi0]
      change v (e (0 + t)) - u b ≤ 0
      simpa only [zero_add] using sub_nonpos.mpr hvt
    simpa [smul_eq_mul] using
      mul_nonpos_of_nonneg_of_nonpos (inv_nonneg.mpr ht.1.le) hdiff
  have hderivnonpos : fderiv Real v b (a - b) ≤ 0 :=
    le_of_tendsto hphideriv.tendsto_slope_zero_right hslope_nonpos
  have hvformula : fderiv Real v b (a - b) =
      eps * (2 * alpha * Real.exp (-alpha * R ^ 2) * R ^ 2) := by
    unfold v barrierFunction
    have hinner : ⟪b - a, a - b⟫_Real = -(R ^ 2) := by
      rw [show a - b = -(b - a) by abel, inner_neg_right, real_inner_self_eq_norm_sq,
        hnorm]
    have hgdiff : DifferentiableAt Real (gaussian a alpha) b :=
      ((gaussian_contDiff a alpha).differentiable (by norm_num)).differentiableAt
    have hqdiff : DifferentiableAt Real
        (fun z => gaussian a alpha z - Real.exp (-alpha * R ^ 2)) b :=
      hgdiff.sub (differentiableAt_const (c := Real.exp (-alpha * R ^ 2)))
    have hqfderiv : fderiv Real
        (fun z => gaussian a alpha z - Real.exp (-alpha * R ^ 2)) b =
        fderiv Real (gaussian a alpha) b := by
      rw [fderiv_fun_sub hgdiff (differentiableAt_const
        (c := Real.exp (-alpha * R ^ 2))), fderiv_const_apply, sub_zero]
    rw [fderiv_fun_add]
    · rw [hufderiv]
      simp only [ContinuousLinearMap.zero_apply, zero_add]
      rw [fderiv_const_mul hqdiff eps, hqfderiv]
      simp only [ContinuousLinearMap.smul_apply, smul_eq_mul]
      rw [fderiv_gaussian_apply, hnorm, hinner]
      ring
    · exact huC2.differentiableAt (by norm_num)
    · exact hqdiff.const_mul eps
  rw [hvformula] at hderivnonpos
  have : 0 < eps * (2 * alpha * Real.exp (-alpha * R ^ 2) * R ^ 2) := by
    positivity
  linarith

end Barrier

namespace Barrier

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace Real E]
  [FiniteDimensional Real E]

theorem tangentBall_geometry
    {Omega : Set E} {u : E -> Real} {y x : E} {rho : Real}
    (hOmega : IsOpen Omega) (hrho : 0 < rho)
    (hclosed : Metric.closedBall y rho ⊆ Omega)
    (huy : ∀ z ∈ Omega, u z ≤ u y)
    (hucont : ContinuousOn u Omega)
    (hxy : x ∈ Metric.ball y (rho / 4)) (hux : u x < u y) :
    ∃ (s : Set E) (b : E) (R : Real),
      x ∈ s ∧ IsOpen s ∧ b ∈ frontier s ∧ R = dist x b ∧
      0 < R ∧ R < rho / 4 ∧
      Metric.ball x R ⊆ s ∧ Metric.closedBall x R ⊆ Omega ∧
      b ∈ Omega ∧ u b = u y ∧ ∀ z ∈ s, u z < u y := by
  let s0 : Set E := {z | u z < u y}
  let s : Set E := s0 ∩ Metric.ball y (rho / 2)
  have hsubOmega : s0 ∩ Metric.ball y (rho / 2) ⊆ Omega := by
    intro z hz
    apply hclosed
    apply Metric.mem_closedBall.mpr
    exact hz.2.le.trans (by linarith)
  have hsopen : IsOpen s := by
    have hpre : IsOpen (Omega ∩ u ⁻¹' Set.Iio (u y)) :=
      hucont.isOpen_inter_preimage hOmega (isOpen_Iio)
    have heq : s = (Omega ∩ u ⁻¹' Set.Iio (u y)) ∩ Metric.ball y (rho / 2) := by
      ext z
      simp only [s, s0, mem_inter_iff, mem_setOf_eq, mem_preimage, mem_Iio]
      constructor
      · intro hz
        exact ⟨⟨hsubOmega hz, hz.1⟩, hz.2⟩
      · tauto
    rw [heq]
    exact hpre.inter Metric.isOpen_ball
  have hxs : x ∈ s := by
    refine ⟨hux, ?_⟩
    exact Metric.mem_ball.mpr (lt_trans hxy (by linarith))
  have hys : y ∉ s := by simp [s, s0]
  have hsne : s ≠ univ := by
    intro h
    exact hys (h ▸ mem_univ y)
  obtain ⟨b, hbfront, hbR⟩ := exists_mem_frontier_infDist_compl_eq_dist hxs hsne
  let R := Metric.infDist x sᶜ
  have hRpos : 0 < R := by
    have hscompl : sᶜ.Nonempty := Set.nonempty_compl.mpr hsne
    apply (hsopen.isClosed_compl.notMem_iff_infDist_pos hscompl).mp
    simpa using hxs
  have hball : Metric.ball x R ⊆ s := Metric.ball_infDist_compl_subset
  have hRxy : R ≤ dist x y := Metric.infDist_le_dist_of_mem hys
  have hRlt : R < rho / 4 := lt_of_le_of_lt hRxy hxy
  have hbxy : dist b y < rho / 2 := by
    calc
      dist b y ≤ dist b x + dist x y := dist_triangle _ _ _
      _ = R + dist x y := by rw [dist_comm b x, ← hbR]
      _ < rho / 2 := by
        have hxy' : dist x y < rho / 4 := hxy
        linarith
  have hbball : b ∈ Metric.ball y (rho / 2) :=
    Metric.mem_ball.mpr (by simpa [dist_comm] using hbxy)
  have hbs0front : b ∈ frontier s0 := by
    have heq := frontier_inter_open_inter (s := s0) (t := Metric.ball y (rho / 2))
      Metric.isOpen_ball
    have : b ∈ frontier s ∩ Metric.ball y (rho / 2) := ⟨hbfront, hbball⟩
    exact (heq ▸ this).1
  have hub : u b = u y := by
    have hbOmega' : b ∈ Omega := by
      apply hclosed
      apply Metric.mem_closedBall.mpr
      linarith
    have huAt : ContinuousAt u b :=
      (hucont b hbOmega').continuousAt (hOmega.mem_nhds hbOmega')
    apply le_antisymm (huy b hbOmega')
    apply le_of_not_gt
    intro hlt
    have hevent : ∀ᶠ z in nhds b, u z < u y :=
      huAt.eventually_lt continuousAt_const hlt
    have hbint : b ∈ interior s0 := by
      rw [mem_interior_iff_mem_nhds]
      simpa [s0] using hevent
    exact (mem_interior_iff_notMem_frontier (interior_subset hbint)).mp hbint hbs0front
  have hbclosed : b ∈ Metric.closedBall y rho := by
    apply Metric.mem_closedBall.mpr
    linarith
  have hbOmega : b ∈ Omega := hclosed hbclosed
  have hclosedOmega : Metric.closedBall x R ⊆ Omega := by
    intro z hz
    apply hclosed
    rw [Metric.mem_closedBall] at hz ⊢
    apply le_of_lt
    calc
      dist z y ≤ dist z x + dist x y := dist_triangle _ _ _
      _ ≤ R + dist x y := by linarith
      _ < rho / 2 := by
        have hxy' : dist x y < rho / 4 := hxy
        linarith
      _ < rho := by linarith
  refine ⟨s, b, R, hxs, hsopen, hbfront, ?_, hRpos, hRlt, hball,
    hclosedOmega, hbOmega, hub, ?_⟩
  · simpa [R] using hbR
  · intro z hz
    exact hz.1

theorem no_strict_drop_in_tangent_neighborhood
    {Omega : Set E} {u : E -> Real} {y x : E} {rho : Real}
    (hOmega : IsOpen Omega) (hyOmega : y ∈ Omega)
    (hclosed : Metric.closedBall y rho ⊆ Omega) (hrho : 0 < rho)
    (hharm : InnerProductSpace.HarmonicOnNhd u Omega)
    (hmax : ∀ z ∈ Omega, u z ≤ u y)
    (hxy : x ∈ Metric.ball y (rho / 4)) : ¬ u x < u y := by
  intro hux
  have hucont : ContinuousOn u Omega := hharm.continuousOn
  obtain ⟨s, b, R, hxs, hsopen, hbfront, hRb, hR, hRrho, hball,
      hclosedOmega, hbOmega, hub, hslt⟩ :=
    tangentBall_geometry hOmega hrho hclosed hmax hucont hxy hux
  have hballlt : ∀ z ∈ Metric.ball x R, u z < u b := by
    intro z hz
    exact (hslt z (hball hz)).trans_eq hub.symm
  have hucontClosed : ContinuousOn u (Metric.closedBall x (R / 2)) :=
    hharm.continuousOn.mono (Metric.closedBall_subset_closedBall (by linarith) |>.trans
      hclosedOmega)
  obtain ⟨m, hum, hinner⟩ := innerBall_uniform_gap hR hucontClosed hballlt
  let alpha : Real := ((Module.finrank Real E : Real) + 1) / (2 * (R / 2) ^ 2)
  have halpha : 0 < alpha := by
    unfold alpha
    positivity
  have halarge : (Module.finrank Real E : Real) < 2 * alpha * (R / 2) ^ 2 := by
    unfold alpha
    field_simp
    nlinarith
  let H : Real := Real.exp (-alpha * (R / 2) ^ 2) - Real.exp (-alpha * R ^ 2)
  have hH : 0 < H := gaussian_barrier_pos_on_inner hR halpha
  let eps : Real := (u b - m) / (2 * H)
  have heps : 0 < eps := by
    unfold eps
    exact div_pos (sub_pos.mpr hum) (mul_pos (by norm_num) hH)
  have hepssmall : eps * H ≤ u b - m := by
    unfold eps
    field_simp
    nlinarith
  have hcomp : ∀ z ∈ annulus x R,
      barrierFunction u x R alpha eps z ≤ u b := by
    have hxyne : x ≠ y := by
      intro h
      subst x
      exact (lt_irrefl (u y)) hux
    haveI : Nontrivial E := ⟨⟨x, y, hxyne⟩⟩
    have hdim : 0 < Module.finrank Real E := Module.finrank_pos
    apply gaussian_annulus_comparison hR
        (by simpa [dist_comm] using hRb.symm) hdim hclosedOmega hharm
        (fun z hz => by simpa [hub] using hmax z hz) rfl hum hinner
        halpha halarge heps
    simpa [H] using hepssmall
  exact tangentBarrier_derivative_contradiction hOmega hbOmega
    (hharm b hbOmega).1 (fun z hz => by simpa [hub] using hmax z hz)
    hR (by simpa [dist_comm] using hRb.symm) halpha heps hcomp

end Barrier

namespace Stage1Instances.THM_M_1140

/-- Harmonicity and an attained maximum force equality on a neighborhood of
the maximizing point. -/
theorem interiorLocalRigidity : InteriorLocalRigidity := by
  intro n Omega u y hOmega hyOmega hharm hmax
  obtain ⟨r, hr, hball⟩ := Metric.mem_nhds_iff.mp (hOmega.mem_nhds hyOmega)
  let rho : Real := r / 2
  have hrho : 0 < rho := by
    dsimp [rho]
    positivity
  have hclosed : Metric.closedBall y rho ⊆ Omega := by
    exact (Metric.closedBall_subset_ball (by dsimp [rho]; linarith)).trans hball
  let V : Set (Space n) := Metric.ball y (rho / 4)
  have hVOmega : V ⊆ Omega := by
    intro z hz
    apply hclosed
    apply Metric.mem_closedBall.mpr
    exact (Metric.mem_ball.mp hz).le.trans (by dsimp [rho]; linarith)
  refine ⟨V, Metric.isOpen_ball, Metric.mem_ball_self (by positivity), hVOmega, ?_⟩
  intro z hz
  apply le_antisymm (hmax z (hVOmega hz))
  apply le_of_not_gt
  exact Barrier.no_strict_drop_in_tangent_neighborhood hOmega hyOmega hclosed hrho
    hharm hmax hz

/-- A nonempty locally constant level set is all of a connected domain. -/
theorem connectedLevelPropagation : ConnectedLevelPropagation := by
  intro n Omega u c hne hopen hconn hcont hexists hlocal
  let level : Set Omega := {x | u x = c}
  have hlevelClosed : IsClosed level := by
    change IsClosed {x : Omega | (Omega.restrict u) x = (fun _ => c) x}
    exact isClosed_eq hcont.restrict continuous_const
  have hlevelOpen : IsOpen level := by
    rw [isOpen_iff_mem_nhds]
    intro y hy
    obtain ⟨V, hVopen, hyV, hVOmega, hVeq⟩ :=
      hlocal y y.property hy
    filter_upwards [hVopen.preimage_val.mem_nhds hyV] with z hz
    exact hVeq z hz
  letI : PreconnectedSpace Omega := Subtype.preconnectedSpace hconn.isPreconnected
  have hlevelNonempty : level.Nonempty := by
    obtain ⟨y, hy, hyc⟩ := hexists
    exact ⟨⟨y, hy⟩, hyc⟩
  have hlevel : level = univ := IsClopen.eq_univ ⟨hlevelClosed, hlevelOpen⟩ hlevelNonempty
  intro x hx
  have hxlevel : (⟨x, hx⟩ : Omega) ∈ level := hlevel.symm.subset (mem_univ _)
  exact hxlevel

/-- Exact strong maximum principle from the analytic and topological packages. -/
theorem harmonicStrongMaximumPrinciple : HarmonicStrongMaximumPrinciple :=
  harmonicStrongMaximumPrinciple_of_packages interiorLocalRigidity connectedLevelPropagation

#print axioms interiorLocalRigidity
#print axioms connectedLevelPropagation
#print axioms harmonicStrongMaximumPrinciple
#print sorries interiorLocalRigidity
#print sorries connectedLevelPropagation
#print sorries harmonicStrongMaximumPrinciple

end Stage1Instances.THM_M_1140
