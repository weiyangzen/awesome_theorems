import Statement
import Mathlib.Analysis.InnerProductSpace.Calculus
import Mathlib.Analysis.InnerProductSpace.GramMatrix
import Mathlib.Analysis.Matrix.Order

/-!
# THM-M-0158 proof

The proof differentiates the unit-normal and orthogonality identities, then uses the
nonsingular first fundamental form to identify the tangential coefficients.
-/

namespace Stage1Instances.THM_M_0158

open scoped RealInnerProductSpace

private theorem inner_partialWithin_self_eq_zero
    (U : Set ParameterSpace) (f : ParameterSpace -> AmbientSpace) (p : ParameterSpace)
    (hp : p ∈ U) (hU : IsOpen U) (hf : DifferentiableWithinAt Real f U p)
    (hunit : forall q, q ∈ U -> ‖f q‖ = 1) (i : Fin 2) :
    @inner Real AmbientSpace _ (f p) (partialWithin U f i p) = 0 := by
  have hd := (hf.hasFDerivWithinAt.norm_sq).congr'
    (f₁ := fun _ => (1 : Real)) (fun q hq => by simp [hunit q hq]) hp
  have hz2 : (2 : Nat) • (innerSL Real (f p)).comp (fderivWithin Real f U p) = 0 := by
    simpa using (hd.fderivWithin (hU.uniqueDiffWithinAt hp)).symm
  have hv2 := congrArg
    (fun (L : ParameterSpace →L[Real] Real) => L (coordinateVector i)) hz2
  change (2 : Nat) • (((innerSL Real (f p)).comp (fderivWithin Real f U p))
    (coordinateVector i)) = 0 at hv2
  have hv : ((innerSL Real (f p)).comp (fderivWithin Real f U p))
      (coordinateVector i) = 0 := by
    simpa [two_nsmul] using hv2
  simpa [partialWithin] using hv

private theorem inner_partialWithin_eq_neg_second
    (U : Set ParameterSpace) (x N : ParameterSpace -> AmbientSpace) (p : ParameterSpace)
    (hp : p ∈ U) (hU : IsOpen U)
    (hx : ContDiffOn Real 2 x U) (hN : ContDiffOn Real 1 N U)
    (horth : forall q, q ∈ U -> forall k : Fin 2,
      @inner Real AmbientSpace _ (N q) (partialWithin U x k q) = 0)
    (i k : Fin 2) :
    @inner Real AmbientSpace _ (partialWithin U x k p) (partialWithin U N i p) =
      -secondFundamentalForm U x N p k i := by
  have hNU : UniqueDiffOn Real U := hU.uniqueDiffOn
  have hxk : ContDiffWithinAt Real 1 (partialWithin U x k) U p := by
    exact (hx p hp).fderivWithin_right_apply contDiffWithinAt_const hNU (by norm_num) hp
  have hd := ((hN p hp).differentiableWithinAt (by norm_num)).hasFDerivWithinAt.inner Real
    (hxk.differentiableWithinAt (by norm_num)).hasFDerivWithinAt
  have hd0 := hd.congr' (f₁ := fun _ => (0 : Real)) (fun q hq => (horth q hq k).symm) hp
  have hz := hd0.fderivWithin (hU.uniqueDiffWithinAt hp)
  have hv := congrArg
    (fun (L : ParameterSpace →L[Real] Real) => L (coordinateVector i)) hz
  simp only [fderivWithin_const_apply, ContinuousLinearMap.zero_apply,
    ContinuousLinearMap.comp_apply, ContinuousLinearMap.prod_apply,
    fderivInnerCLM_apply, partialWithin] at hv
  have hv' := (eq_neg_of_add_eq_zero_right hv.symm)
  simpa [secondFundamentalForm, real_inner_comm] using hv'

theorem weingartenEquations : WeingartenEquationsTarget := by
  intro U x N p hU hp hx hN hunit horth hdet i
  let I := firstFundamentalForm U x p
  let II := secondFundamentalForm U x N p
  let c : Fin 2 -> Real := fun j => (-(I⁻¹ * II)) j i
  let rhs : AmbientSpace := ∑ j : Fin 2, c j • partialWithin U x j p
  have hNdiff : DifferentiableWithinAt Real N U p :=
    (hN p hp).differentiableWithinAt (by norm_num)
  have hnormal : @inner Real AmbientSpace _ (N p) (partialWithin U N i p) = 0 :=
    inner_partialWithin_self_eq_zero U N p hp hU hNdiff hunit i
  have hnormal_rhs : @inner Real AmbientSpace _ (N p) rhs = 0 := by
    simp only [rhs, inner_sum, inner_smul_right]
    simp [horth p hp]
  have hrow (k : Fin 2) :
      @inner Real AmbientSpace _ (partialWithin U x k p) (partialWithin U N i p) = -II k i :=
    inner_partialWithin_eq_neg_second U x N p hp hU hx hN horth i k
  have hc (k : Fin 2) : ∑ j : Fin 2, I k j * c j = -II k i := by
    have hunit : IsUnit I.det := isUnit_iff_ne_zero.mpr hdet
    calc
      ∑ j, I k j * c j = (I * (-(I⁻¹ * II))) k i := by simp [c, Matrix.mul_apply]
      _ = -II k i := by
        have hm : I * (I⁻¹ * II) = II := by
          rw [← Matrix.mul_assoc, Matrix.mul_nonsing_inv _ hunit, one_mul]
        rw [Matrix.mul_neg, hm]
        rfl
  have hrow_rhs (k : Fin 2) : @inner Real AmbientSpace _ (partialWithin U x k p) rhs = -II k i := by
    simp only [rhs, inner_sum]
    calc
      _ = ∑ j : Fin 2, c j * I k j := by
        simp [rhs, real_inner_smul_right, I, firstFundamentalForm]
      _ = -II k i := by simpa [mul_comm] using hc k
  have hspan : LinearIndependent Real (fun k : Fin 2 => partialWithin U x k p) := by
    apply Matrix.linearIndependent_of_posDef_gram
    apply (Matrix.posSemidef_gram Real _).posDef_iff_isUnit.mpr
    rw [Matrix.isUnit_iff_isUnit_det, isUnit_iff_ne_zero]
    simpa [I, firstFundamentalForm, Matrix.gram, real_inner_comm] using hdet
  let v : Fin 3 -> AmbientSpace :=
    Fin.cons (N p) (fun j : Fin 2 => partialWithin U x j p)
  have hli : LinearIndependent Real v := by
    apply LinearIndependent.fin_cons hspan
    intro hmem
    obtain ⟨a, ha⟩ := (Submodule.mem_span_range_iff_exists_fun Real).mp hmem
    have heq := congrArg (fun v : AmbientSpace => @inner Real AmbientSpace _ (N p) v) ha
    have hnorm : @inner Real AmbientSpace _ (N p) (N p) = 1 := by
      simpa [hunit p hp] using (real_inner_self_eq_norm_sq (N p))
    have hleft : @inner Real AmbientSpace _ (N p)
        (∑ j : Fin 2, a j • partialWithin U x j p) = 0 := by
      rw [inner_sum]
      apply Finset.sum_eq_zero
      intro j hj
      rw [real_inner_smul_right, horth p hp j, mul_zero]
    exact zero_ne_one (hleft.symm.trans (heq.trans hnorm))
  let b : Module.Basis (Fin 3) Real AmbientSpace :=
    basisOfLinearIndependentOfCardEqFinrank hli (by
      simp [AmbientSpace])
  have heq : partialWithin U N i p = rhs := by
    apply ext_inner_left Real
    intro z
    rw [← b.sum_repr z]
    simp only [sum_inner, inner_smul_left]
    apply Finset.sum_congr rfl
    intro k hk
    congr 1
    rw [show b k = v k by
      simpa [b] using congrFun (coe_basisOfLinearIndependentOfCardEqFinrank hli
        (by simp [AmbientSpace])) k]
    refine Fin.cases ?_ (fun j => ?_) k
    · exact hnormal.trans hnormal_rhs.symm
    · exact (hrow j).trans (hrow_rhs j).symm
  simpa [rhs, c, I, II, add_comm] using heq

#print axioms weingartenEquations

end Stage1Instances.THM_M_0158
