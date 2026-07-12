import ObligationTree

/-!
# THM-M-1288 proof-phase bodies

This module proves the elementary domain, gradient-transport, and zero-branch
leaves of the frozen Talenti obligation tree.  The sharp analytic estimate and
optimality argument remain explicit package premises; no root closure is
claimed here.
-/

noncomputable section

open MeasureTheory
open scoped ContDiff Gradient

namespace Stage1Instances.THM_M_1288

/-- Domain consequences used by the analytic and sharpness subtrees. -/
theorem domain_facts (n : Nat) (p : Real) (hp : 1 < p) (hpn : p < (n : Real)) :
    2 <= n /\ 0 < p /\ 0 < (n : Real) - p := by
  have hn : 1 < n := by exact_mod_cast hp.trans hpn
  exact ⟨hn, lt_trans (by norm_num) hp, sub_pos.mpr hpn⟩

/-- For a differentiable scalar function, the total gradient and Frechet
derivative have exactly the same norm.  This is the pointwise bridge needed to
reconcile the frozen gradient expression with mathlib's Sobolev API. -/
theorem norm_gradient_eq_norm_fderiv {n : Nat} (u : Space n -> Real)
    (x : Space n) :
    ‖gradient u x‖ = ‖fderiv Real u x‖ := by
  simp only [gradient]
  exact (InnerProductSpace.toDual Real (Space n)).symm.norm_map _

/-- The pointwise gradient/Frechet bridge lifts directly through the frozen
real integral-power norm. -/
theorem vectorLpNorm_gradient_eq_fderiv {n : Nat} (p : Real)
    (u : Space n -> Real) :
    vectorLpNorm p (gradient u) =
      (integral volume (fun x => ‖fderiv Real u x‖ ^ p)) ^ (1 / p) := by
  simp only [vectorLpNorm, norm_gradient_eq_norm_fderiv]

/-- The scalar frozen norm of the zero test function is zero. -/
theorem lpNorm_zero (n : Nat) (q : Real) (hq : q ≠ 0) :
    lpNorm (n := n) q (fun _ => 0) = 0 := by
  simp [lpNorm, Real.zero_rpow hq, inv_ne_zero hq]

/-- The vector frozen norm of the gradient of the zero test function is zero. -/
theorem vectorLpNorm_gradient_zero (n : Nat) (p : Real) (hp : p ≠ 0) :
    vectorLpNorm (n := n) p (gradient (fun _ => (0 : Real))) = 0 := by
  simp [vectorLpNorm, gradient, Real.zero_rpow hp, inv_ne_zero hp]

/-- The zero branch of admissibility closes for every proposed constant. -/
theorem zero_test_function_branch (n : Nat) (p C : Real)
    (hp : 1 < p) (hpn : p < (n : Real)) :
    lpNorm (sobolevConjugate n p) (fun _ : Space n => 0) <=
      C * vectorLpNorm (n := n) p
        (gradient (𝕜 := Real) (fun _ : Space n => 0)) := by
  have hp0 : p ≠ 0 := ne_of_gt (lt_trans (by norm_num) hp)
  have hn0 : (n : Real) ≠ 0 := ne_of_gt ((lt_trans (by norm_num) hp).trans hpn)
  have hden : (n : Real) - p ≠ 0 := ne_of_gt (sub_pos.mpr hpn)
  have hq0 : sobolevConjugate n p ≠ 0 := by
    simp only [sobolevConjugate]
    exact div_ne_zero (mul_ne_zero hn0 hp0) hden
  rw [lpNorm_zero n _ hq0, vectorLpNorm_gradient_zero n p hp0, mul_zero]

/-- Root composition after the two genuinely analytic packages have been
supplied.  The arguments deliberately remain visible in the theorem type. -/
theorem talentiSharpSobolevTarget_of_open_analytic_packages
    (admissibility : TalentiAdmissibilityPackage)
    (optimality : TalentiOptimalityPackage) : TalentiSharpSobolevTarget :=
  talentiSharpSobolevTarget_of_packages admissibility optimality

#print axioms domain_facts
#print axioms norm_gradient_eq_norm_fderiv
#print axioms vectorLpNorm_gradient_eq_fderiv
#print axioms lpNorm_zero
#print axioms vectorLpNorm_gradient_zero
#print axioms zero_test_function_branch
#print axioms talentiSharpSobolevTarget_of_open_analytic_packages

end Stage1Instances.THM_M_1288
