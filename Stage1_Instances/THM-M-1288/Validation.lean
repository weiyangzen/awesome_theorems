import Statement

/-!
# THM-M-1288 independent local validation probes

This module intentionally imports neither `ObligationTree` nor `Proof`.  It
reconstructs the conditional root interface and representative bounded leaves
directly from the frozen statement.  It does not supply either open sharp
analytic package.
-/

noncomputable section

open MeasureTheory
open scoped ContDiff Gradient

namespace Stage1Instances.THM_M_1288.Validation

def IndependentAdmissibilityPackage : Prop :=
  forall (n : Nat) (p : Real),
    1 < p -> p < (n : Real) ->
      IsAdmissibleConstant n p (talentiConstant n p)

def IndependentOptimalityPackage : Prop :=
  forall (n : Nat) (p : Real),
    1 < p -> p < (n : Real) ->
      forall C : Real, IsAdmissibleConstant n p C -> talentiConstant n p <= C

/-- Differential reconstruction of the exact conditional root composition. -/
theorem independentlyComposeRoot
    (admissibility : IndependentAdmissibilityPackage)
    (optimality : IndependentOptimalityPackage) : TalentiSharpSobolevTarget := by
  intro n p hp hpn
  exact ⟨admissibility n p hp hpn, optimality n p hp hpn⟩

/-- Differential reconstruction of the elementary domain facts. -/
theorem independentlyCheckDomain (n : Nat) (p : Real)
    (hp : 1 < p) (hpn : p < (n : Real)) :
    2 <= n /\ 0 < p /\ 0 < (n : Real) - p := by
  have hn : 1 < n := by exact_mod_cast hp.trans hpn
  exact ⟨hn, lt_trans (by norm_num) hp, sub_pos.mpr hpn⟩

/-- Differential reconstruction of the gradient/Frechet norm bridge. -/
theorem independentlyCheckGradient {n : Nat} (u : Space n -> Real)
    (x : Space n) :
    ‖gradient u x‖ = ‖fderiv Real u x‖ := by
  simp only [gradient]
  exact (InnerProductSpace.toDual Real (Space n)).symm.norm_map _

/-- Differential reconstruction of the scalar zero-expression boundary. -/
theorem independentlyCheckZeroLpNorm (n : Nat) (q : Real) (hq : q ≠ 0) :
    lpNorm (n := n) q (fun _ => 0) = 0 := by
  simp [lpNorm, Real.zero_rpow hq, inv_ne_zero hq]

#print axioms independentlyComposeRoot
#print axioms independentlyCheckDomain
#print axioms independentlyCheckGradient
#print axioms independentlyCheckZeroLpNorm

end Stage1Instances.THM_M_1288.Validation
