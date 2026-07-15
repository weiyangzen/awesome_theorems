import Mathlib
import Statement

/-!
# THM-M-0161: checked obstruction to the frozen target

The frozen statement asks a `C^3` curve to realize every differentiable
positive curvature. Such a realization forces the curvature to be `C^1`.
The function `kappa161` below is positive and differentiable on `(-1, 1)`,
but its derivative is discontinuous at zero. Consequently the target is false.

This refutes only the frozen Lean encoding, whose `DifferentiableOn`
coefficient hypothesis is weaker than the usual textbook `C^1` convention.
It does not refute the classical fundamental theorem of space curves.
-/

namespace Stage1Instances.THM_M_0161

open Set Filter Topology

theorem curvature_is_contDiffOn_one
    {a b : Real} {kappa : Real → Real} {c : Real → E3}
    (hc : ContDiffOn Real 3 c (Ioo a b))
    (hcurv : ∀ s ∈ Ioo a b, curvature a b c s = kappa s)
    (hpositive : ∀ s ∈ Ioo a b, 0 < kappa s) :
    ContDiffOn Real 1 kappa (Ioo a b) := by
  have hd1 : ContDiffOn Real 2 (dWithin a b c) (Ioo a b) := by
    exact hc.derivWithin (uniqueDiffOn_Ioo a b) (by norm_num)
  have hd2 : ContDiffOn Real 1 (d2Within a b c) (Ioo a b) := by
    exact hd1.derivWithin (uniqueDiffOn_Ioo a b) (by norm_num)
  have hdot : ContDiffOn Real 1
      (fun s => dot (d2Within a b c s) (d2Within a b c s)) (Ioo a b) := by
    apply ContDiffOn.sum
    intro i hi
    exact ((contDiffOn_pi.mp hd2) i).mul ((contDiffOn_pi.mp hd2) i)
  have hdot_ne : ∀ s ∈ Ioo a b,
      dot (d2Within a b c s) (d2Within a b c s) ≠ 0 := by
    intro s hs hzero
    have hzero' : curvature a b c s = 0 := by
      simp [curvature, length, hzero]
    linarith [hpositive s hs, hcurv s hs]
  have hlen : ContDiffOn Real 1
      (fun s => length (d2Within a b c s)) (Ioo a b) := by
    exact hdot.sqrt hdot_ne
  apply hlen.congr
  intro s hs
  exact (hcurv s hs).symm

noncomputable def bad161 (x : Real) : Real :=
  x ^ 2 * Real.sin (1 / x)

lemma bad161_hasDerivAt_zero : HasDerivAt bad161 0 0 := by
  rw [hasDerivAt_iff_isLittleO_nhds_zero]
  have hpow : (fun x : Real => x ^ 2) =o[nhds 0] fun x => x := by
    simpa using Asymptotics.isLittleO_pow_id (𝕜 := Real) (by norm_num : 1 < 2)
  have hsin : (fun x : Real => Real.sin (1 / x)) =O[nhds 0] fun _ => (1 : Real) :=
    Asymptotics.IsBigO.of_bound 1 <|
      Filter.Eventually.of_forall fun x => by
        simpa [Real.norm_eq_abs] using Real.abs_sin_le_one (1 / x)
  simpa [bad161] using hpow.mul_isBigO hsin

lemma bad161_hasDerivAt_of_ne {x : Real} (hx : x ≠ 0) :
    HasDerivAt bad161 (2 * x * Real.sin (1 / x) - Real.cos (1 / x)) x := by
  have hinv : HasDerivAt (fun y : Real => 1 / y) (-(1 / x ^ 2)) x := by
    simpa [one_div] using hasDerivAt_inv (𝕜 := Real) hx
  have hsin : HasDerivAt (fun y : Real => Real.sin (1 / y))
      (Real.cos (1 / x) * (-(1 / x ^ 2))) x :=
    (Real.hasDerivAt_sin (1 / x)).comp x hinv
  have hraw := ((hasDerivAt_id (𝕜 := Real) (x := x)).pow 2).mul hsin
  convert hraw using 1 <;> simp only [id_eq, Pi.pow_apply]
  field_simp [hx]
  ring

lemma bad161_differentiable : Differentiable Real bad161 := by
  intro x
  by_cases hx : x = 0
  · simpa [hx] using bad161_hasDerivAt_zero.differentiableAt
  · exact (bad161_hasDerivAt_of_ne hx).differentiableAt

lemma deriv_bad161_zero : deriv bad161 0 = 0 :=
  bad161_hasDerivAt_zero.deriv

lemma deriv_bad161_of_ne {x : Real} (hx : x ≠ 0) :
    deriv bad161 x = 2 * x * Real.sin (1 / x) - Real.cos (1 / x) :=
  (bad161_hasDerivAt_of_ne hx).deriv

noncomputable def seq161 (n : Nat) : Real :=
  1 / ((n + 1 : Nat) * (2 * Real.pi))

lemma seq161_pos (n : Nat) : 0 < seq161 n := by
  unfold seq161
  positivity

lemma seq161_ne (n : Nat) : seq161 n ≠ 0 :=
  (seq161_pos n).ne'

lemma one_div_seq161 (n : Nat) :
    1 / seq161 n = (n + 1 : Nat) * (2 * Real.pi) := by
  unfold seq161
  field_simp

lemma deriv_bad161_seq (n : Nat) :
    deriv bad161 (seq161 n) = 2 * seq161 n * Real.sin (1 / seq161 n) - 1 := by
  rw [deriv_bad161_of_ne (seq161_ne n), one_div_seq161,
    Real.cos_nat_mul_two_pi]

lemma sin_one_div_seq161 (n : Nat) : Real.sin (1 / seq161 n) = 0 := by
  rw [one_div_seq161]
  have := Real.sin_add_nat_mul_two_pi 0 (n + 1)
  simpa using this

lemma deriv_bad161_seq_eq (n : Nat) : deriv bad161 (seq161 n) = -1 := by
  rw [deriv_bad161_seq, sin_one_div_seq161]
  ring

lemma seq161_tendsto : Tendsto seq161 atTop (nhds 0) := by
  unfold seq161
  have hdenom : Tendsto (fun n : Nat => ((n + 1 : Nat) : Real) * (2 * Real.pi))
      atTop atTop := by
    apply Filter.Tendsto.atTop_mul_const (by positivity)
    exact tendsto_natCast_atTop_atTop.comp (tendsto_add_atTop_nat 1)
  simpa [Function.comp_def, one_div] using tendsto_inv_atTop_zero.comp hdenom

lemma bad161_deriv_not_continuousAt : Not (ContinuousAt (deriv bad161) 0) := by
  intro hcont
  have hto0 : Tendsto (fun n => deriv bad161 (seq161 n)) atTop (nhds 0) := by
    simpa [deriv_bad161_zero] using hcont.tendsto.comp seq161_tendsto
  have htoneg : Tendsto (fun n => deriv bad161 (seq161 n)) atTop (nhds (-1)) := by
    simpa only [deriv_bad161_seq_eq] using tendsto_const_nhds
  have : (0 : Real) = -1 := tendsto_nhds_unique hto0 htoneg
  norm_num at this

lemma bad161_not_contDiffAt_one : Not (ContDiffAt Real 1 bad161 0) := by
  intro h
  rw [contDiffAt_one_iff] at h
  obtain ⟨f', u, hu, hf'cont, hf'⟩ := h
  have heq : (fun x => (f' x) 1) =ᶠ[nhds 0] deriv bad161 := by
    filter_upwards [hu] with x hx
    exact (hf' x hx).hasDerivAt.deriv.symm
  have hleft : Tendsto (fun x => (f' x) 1) (nhds 0) (nhds ((f' 0) 1)) := by
    exact ((hf'cont.continuousAt hu).clm_apply continuousAt_const).tendsto
  have hright : Tendsto (deriv bad161) (nhds 0) (nhds ((f' 0) 1)) :=
    hleft.congr' heq
  have hzero : (f' 0) 1 = 0 := by
    have heq0 := (hf' 0 (mem_of_mem_nhds hu)).hasDerivAt.deriv
    linarith [heq0, deriv_bad161_zero]
  exact bad161_deriv_not_continuousAt (by
    rw [ContinuousAt]
    simpa [hzero, deriv_bad161_zero] using hright)

noncomputable def kappa161 (x : Real) : Real :=
  2 + bad161 x

lemma abs_bad161_le_sq (x : Real) : abs (bad161 x) ≤ x ^ 2 := by
  rw [bad161, abs_mul, abs_sq]
  have hsin := Real.abs_sin_le_one (1 / x)
  nlinarith [sq_nonneg x]

lemma bad161_gt_neg_one_of_mem {x : Real} (hx : x ∈ Ioo (-1 : Real) 1) :
    -1 < bad161 x := by
  have hsquare : x ^ 2 < 1 := by
    nlinarith [hx.1, hx.2]
  have habs := abs_bad161_le_sq x
  have hnegabs : -abs (bad161 x) ≤ bad161 x := neg_abs_le (bad161 x)
  linarith

lemma kappa161_pos_of_mem {x : Real} (hx : x ∈ Ioo (-1 : Real) 1) :
    0 < kappa161 x := by
  unfold kappa161
  linarith [bad161_gt_neg_one_of_mem hx]

lemma kappa161_differentiable : Differentiable Real kappa161 := by
  exact differentiable_const 2 |>.add bad161_differentiable

lemma kappa161_not_contDiffAt_one : Not (ContDiffAt Real 1 kappa161 0) := by
  intro h
  have hbad : ContDiffAt Real 1 bad161 0 := by
    have hconst : ContDiffAt Real 1 (fun _ : Real => (2 : Real)) 0 := contDiffAt_const
    simpa only [kappa161, add_sub_cancel_left] using h.sub hconst
  exact bad161_not_contDiffAt_one hbad

lemma kappa161_not_contDiffOn_one :
    Not (ContDiffOn Real 1 kappa161 (Ioo (-1 : Real) 1)) := by
  intro h
  have hlocal := h 0 (by norm_num : (0 : Real) ∈ Ioo (-1 : Real) 1)
  have hat : ContDiffAt Real 1 kappa161 0 :=
    hlocal.contDiffAt (Ioo_mem_nhds (by norm_num) (by norm_num))
  exact kappa161_not_contDiffAt_one hat

/-- The exact frozen target is refuted by a differentiable positive curvature
that cannot be the curvature of a `C^3` realizing curve. -/
theorem frozen_target_false : Not FundamentalTheoremOfSpaceCurvesTarget := by
  intro htarget
  have hresult := htarget (-1) 1 (by norm_num) kappa161 (fun _ => (0 : Real))
    kappa161_differentiable.differentiableOn
    (differentiable_const (0 : Real)).differentiableOn
    (fun s hs => kappa161_pos_of_mem hs)
  obtain ⟨c, hc⟩ := hresult.1
  have hsmooth : ContDiffOn Real 1 kappa161 (Ioo (-1 : Real) 1) :=
    curvature_is_contDiffOn_one hc.1 hc.2.2.1 (fun s hs => kappa161_pos_of_mem hs)
  exact kappa161_not_contDiffOn_one hsmooth

#check curvature_is_contDiffOn_one
#check frozen_target_false
#print axioms curvature_is_contDiffOn_one
#print axioms frozen_target_false

end Stage1Instances.THM_M_0161
