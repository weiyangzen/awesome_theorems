import ObligationTree
import Mathlib.Analysis.Calculus.DerivativeTest
import Mathlib.Analysis.InnerProductSpace.Calculus
import Mathlib.Topology.Connected.Clopen

/-!
# THM-M-1138 proof

The proof uses a strictly subharmonic perturbation `u + epsilon * normSq`.
A positive perturbation cannot have an interior local maximum, because its
Laplacian is positive there. Compactness then places a perturbed maximum on
the frontier, and sending the perturbation coefficient to zero proves the
weak maximum principle.
-/

open Set Topology Filter
open InnerProductSpace

namespace Stage1Instances.THM_M_1138.Proof

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

theorem laplacian_norm_sq (x : E) :
    Laplacian.laplacian (fun z : E => ‖z‖ ^ 2) x = 2 * Module.finrank Real E := by
  rw [InnerProductSpace.laplacian_eq_iteratedFDeriv_stdOrthonormalBasis]
  have hdir (i : Fin (Module.finrank Real E)) :
      iteratedFDeriv Real 2 (fun z : E => ‖z‖ ^ 2) x
          ![(stdOrthonormalBasis Real E) i, (stdOrthonormalBasis Real E) i] = 2 := by
    rw [iteratedFDeriv_two_apply]
    rw [fderiv_norm_sq]
    change fderiv Real (fun z : E => 2 • innerSL Real z) x _ _ = 2
    have hfun : (fun z : E => 2 • innerSL Real z) =
        (((2 : Real) • innerSL Real (E := E)).toContinuousLinearMap :
          E -> E →L[Real] Real) := by
      ext z w
      simp only [Pi.smul_apply, ContinuousLinearMap.coe_smul', innerSL_apply_apply,
        LinearMap.coe_toContinuousLinearMap']
      change 2 • ⟪z, w⟫_Real = ((2 • (innerSL Real (E := E))).toLinearMap z) w
      simp [LinearMap.smul_apply]
    rw [hfun]
    rw [(((2 : Real) • innerSL Real (E := E)).toContinuousLinearMap).hasFDerivAt.fderiv]
    change 2 * ⟪(stdOrthonormalBasis Real E) i, (stdOrthonormalBasis Real E) i⟫_Real = 2
    simp
  change (∑ i, iteratedFDeriv Real 2 (fun z : E => ‖z‖ ^ 2) x
      ![(stdOrthonormalBasis Real E) i, (stdOrthonormalBasis Real E) i]) = _
  simp_rw [hdir]
  rw [Finset.sum_const, nsmul_eq_mul]
  simpa only [Finset.card_univ, Fintype.card_fin] using
    (mul_comm (Module.finrank Real E : Real) 2)

theorem strict_subharmonic_not_isLocalMax {u : E -> Real} {x : E}
    (hu : InnerProductSpace.HarmonicAt u x) {ε : Real} (hε : 0 < ε)
    (hdim : 0 < Module.finrank Real E) :
    ¬ IsLocalMax (fun z => u z + ε * ‖z‖ ^ 2) x := by
  intro hmax
  let q : E -> Real := fun z => ε * ‖z‖ ^ 2
  have hnorm : ContDiffAt Real 2 q x := by
    change ContDiffAt Real 2 (ε • fun z : E => ‖z‖ ^ 2) x
    exact (contDiff_norm_sq Real).contDiffAt.const_smul ε
  have hv : ContDiffAt Real 2 (u + q) x := hu.1.add hnorm
  have hmax' : IsLocalMax (u + q) x := by
    simpa [q, Pi.add_apply] using hmax
  have hle := isLocalMax_laplacian_nonpos hv hmax'
  rw [hu.1.laplacian_add hnorm] at hle
  have hulap : Laplacian.laplacian u x = 0 := hu.2.self_of_nhds
  rw [hulap, zero_add] at hle
  have hq : q = ε • (fun z : E => ‖z‖ ^ 2) := by
    ext z
    simp [q]
  rw [hq] at hle
  rw [InnerProductSpace.laplacian_smul ε (contDiff_norm_sq Real).contDiffAt] at hle
  rw [laplacian_norm_sq] at hle
  have hpos : 0 < ε * (2 * (Module.finrank Real E : Real)) := by positivity
  norm_num at hle
  linarith

theorem perturbed_maximizer_mem_frontier {U : Set E} {u : E -> Real}
    (hUopen : IsOpen U) (hu : InnerProductSpace.HarmonicOnNhd u U)
    (hdim : 0 < Module.finrank Real E) {ε : Real} (hε : 0 < ε) {y : E}
    (hycl : y ∈ closure U)
    (hymax : IsMaxOn (fun z => u z + ε * ‖z‖ ^ 2) (closure U) y) :
    y ∈ frontier U := by
  rw [closure_eq_self_union_frontier] at hycl
  rcases hycl with hyU | hyfr
  · have hlocal : IsLocalMax (fun z => u z + ε * ‖z‖ ^ 2) y := by
      apply hymax.isLocalMax
      filter_upwards [hUopen.mem_nhds hyU] with z hz
      exact subset_closure hz
    exfalso
    exact (strict_subharmonic_not_isLocalMax (hu y hyU) hε hdim) hlocal
  · exact hyfr

theorem frontier_nonempty_of_bounded {U : Set E} (hU : U.Nonempty)
    (hUbdd : Bornology.IsBounded U) (hdim : 0 < Module.finrank Real E) :
    (frontier U).Nonempty := by
  haveI : Nontrivial E := Module.nontrivial_of_finrank_pos hdim
  rw [nonempty_frontier_iff]
  exact ⟨hU, fun hUuniv => NormedSpace.unbounded_univ Real E (hUuniv ▸ hUbdd)⟩

theorem boundary_maximum_of_perturbed_maxima {U : Set E} {u : E -> Real}
    (hUopen : IsOpen U) (hU : U.Nonempty)
    (hUbdd : Bornology.IsBounded U) (hu : InnerProductSpace.HarmonicContOnCl u U)
    (hdim : 0 < Module.finrank Real E) :
    ∃ y ∈ frontier U, ∀ x ∈ closure U, u x <= u y := by
  have hcompact : IsCompact (closure U) := hUbdd.isCompact_closure
  have hfrontier : (frontier U).Nonempty := frontier_nonempty_of_bounded hU hUbdd hdim
  have hfrontierCompact : IsCompact (frontier U) :=
    hcompact.of_isClosed_subset isClosed_frontier frontier_subset_closure
  obtain ⟨y, hyfrontier, hymax⟩ :=
    hfrontierCompact.exists_isMaxOn hfrontier (hu.continuousOn.mono frontier_subset_closure)
  obtain ⟨R, hRpos, hR⟩ := hUbdd.closure.exists_pos_norm_le
  refine ⟨y, hyfrontier, ?_⟩
  intro x hxcl
  apply le_of_forall_pos_le_add
  intro δ hδ
  obtain ⟨n, hn⟩ := exists_nat_one_div_lt (div_pos hδ (sq_pos_of_pos hRpos))
  let ε : Real := 1 / (n + 1 : Real)
  have hε : 0 < ε := by positivity
  have hvcont : ContinuousOn (fun z => u z + ε * ‖z‖ ^ 2) (closure U) := by
    have hq : Continuous (fun z : E => ε * ‖z‖ ^ 2) := by
      fun_prop
    exact hu.continuousOn.add hq.continuousOn
  obtain ⟨z, hzcl, hzmax⟩ := hcompact.exists_isMaxOn hU.closure hvcont
  have hzfrontier : z ∈ frontier U :=
    perturbed_maximizer_mem_frontier hUopen hu.harmonicOnNhd hdim hε hzcl hzmax
  have hzle : u z <= u y := hymax hzfrontier
  have hxle := hzmax hxcl
  have hzR : ‖z‖ <= R := hR z hzcl
  have hepsR : ε * R ^ 2 < δ := by
    have hRsq : 0 < R ^ 2 := sq_pos_of_pos hRpos
    exact (lt_div_iff₀ hRsq).mp (by simpa [ε] using hn)
  have hepsnorm : ε * ‖z‖ ^ 2 < δ := by
    have hzsq : ‖z‖ ^ 2 <= R ^ 2 := by nlinarith [norm_nonneg z]
    nlinarith
  change u x + ε * ‖x‖ ^ 2 <= u z + ε * ‖z‖ ^ 2 at hxle
  nlinarith [mul_nonneg hε.le (sq_nonneg ‖x‖)]

theorem boundaryMaximumPackage : BoundaryMaximumPackage := by
  intro n U u hn hU hUopen _hUconnected hUbdd hu
  have hdim : 0 < Module.finrank Real (Space n) := by
    simpa [Space] using hn
  exact boundary_maximum_of_perturbed_maxima hUopen hU hUbdd hu hdim

theorem harmonicWeakMaximumPrinciple : HarmonicWeakMaximumPrinciple :=
  root_of_boundaryMaximumPackage boundaryMaximumPackage

#print sorries boundaryMaximumPackage
#print axioms boundaryMaximumPackage
#print sorries harmonicWeakMaximumPrinciple
#print axioms harmonicWeakMaximumPrinciple

end Stage1Instances.THM_M_1138.Proof
