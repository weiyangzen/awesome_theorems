import Statement

/-!
# THM-M-1241 counterexample to the frozen target

The endpoint `n = m = r = 1`, `j = 0`, `q = p = infinity`, and `a = 1`
admits the constant function `u = 1`. Its first derivative has zero `L^1`
seminorm while its zeroth derivative has nonzero `L^infinity` seminorm.
-/

noncomputable section

open MeasureTheory
open scoped ENNReal

namespace Stage1Instances.THM_M_1241

private theorem derivativeLpNorm_const_zero :
    derivativeLpNorm 0 (⊤ : ENNReal) (fun _ : Space 1 => (1 : Real)) = 1 := by
  simp only [derivativeLpNorm]
  simp_rw [show forall directions : Fin 0 -> Fin 1,
      coordinateDerivative (fun _ : Space 1 => (1 : Real)) directions = fun _ => 1 by
    intro directions
    funext x
    rfl]
  rw [eLpNorm_exponent_top, eLpNormEssSup_const (1 : Real) (NeZero.ne volume)]
  simp

private theorem derivativeLpNorm_const_one :
    derivativeLpNorm 1 1 (fun _ : Space 1 => (1 : Real)) = 0 := by
  simp only [derivativeLpNorm]
  simp_rw [show forall directions : Fin 1 -> Fin 1,
      coordinateDerivative (fun _ : Space 1 => (1 : Real)) directions = fun _ => 0 by
    intro directions
    funext x
    simp only [coordinateDerivative, iteratedFDeriv_const_of_ne one_ne_zero]
    rfl]
  simp

theorem not_gagliardoNirenbergTarget : ¬ GagliardoNirenbergTarget := by
  intro target
  obtain ⟨C, hC⟩ := target 1 1 0 ⊤ 1 ⊤ 1
    (by norm_num)
    (by norm_num)
    (by simp)
    (by norm_num)
    (by simp [reciprocalExponent])
    (by norm_num)
    (by norm_num)
    (by simp)
  have bound := hC (fun _ : Space 1 => (1 : Real))
    (contDiff_const)
    (by simp [derivativeLpNorm_const_zero])
    (by simp [derivativeLpNorm_const_one])
    (by norm_num)
  rw [derivativeLpNorm_const_zero, derivativeLpNorm_const_one] at bound
  norm_num at bound

#print axioms not_gagliardoNirenbergTarget
#print sorries not_gagliardoNirenbergTarget

end Stage1Instances.THM_M_1241
