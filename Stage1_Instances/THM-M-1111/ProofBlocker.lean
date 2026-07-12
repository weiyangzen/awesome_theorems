import Statement
import Mathlib.Tactic

/-!
# THM-M-1111 proof-phase blocker

The frozen target quantifies over an unconstrained semantic interface.  This
module gives a kernel-checked instance for which that exact target is false.
-/

namespace Stage1Instances.THM_M_1111

private def counterSemantics : FourMomentSemantics where
  Ensemble := fun _ => Unit
  Observable := fun _ => Unit
  obeysC0 := fun _ _ _ => True
  offDiagonalMatch := fun _ _ _ _ _ => True
  diagonalMatch := fun _ _ _ _ => True
  smooth := fun _ => True
  derivativeBound := fun _ _ _ => True
  expectedEigenvalueStatistic := fun _ _ _ => 0
  powerBound := fun _ _ => -1

/-- The exact frozen target is not valid for every `FourMomentSemantics`. -/
theorem not_taoVuFourMomentTarget_counterSemantics :
    ¬ TaoVuFourMomentTarget counterSemantics := by
  intro target
  rcases target with ⟨c0, hc0, target⟩
  specialize target (1 / 2 : ℝ) (by norm_num) (by norm_num) 1 (by omega)
  specialize target 1 1 (by norm_num) (by norm_num)
  rcases target with ⟨N, target⟩
  let n := 2 * (N + 1)
  specialize target n (by dsimp [n]; omega) () () trivial trivial
  specialize target (by intros; trivial) (by intros; trivial) () trivial
  specialize target (by intros; trivial)
  let indices : Fin 1 → Fin n := fun _ => ⟨N + 1, by dsimp [n]; omega⟩
  specialize target indices (by
    intro r s hrs
    fin_cases r
    fin_cases s
    simp at hrs)
  specialize target (by
    intro r
    fin_cases r
    constructor <;> dsimp [indices, n] <;>
      push_cast <;> ring_nf <;> rfl)
  norm_num [counterSemantics] at target

#print axioms not_taoVuFourMomentTarget_counterSemantics

end Stage1Instances.THM_M_1111
