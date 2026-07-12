import Mathlib.Analysis.Calculus.FDeriv.Add

import Statement

/-!
# THM-M-1131 independent validation probe

This module deliberately imports neither `Proof` nor `ObligationTree`. It
reconstructs the exact canonical target directly, providing a second local
proof path for differential validation of the proof-phase artifact.
-/

noncomputable section

namespace Stage1Instances.THM_M_1131.Validation

open Stage1Instances.THM_M_1131

private theorem derivative_of_constant_multiple {n : Nat} (c : Real)
    (f : Space n -> Real) (x v : Space n) :
    fderiv Real (fun y => c * f y) x v = c * fderiv Real f x v := by
  have h := congrFun (fderiv_const_smul_field (𝕜 := Real) (f := f) c) x
  simpa [Pi.smul_apply] using DFunLike.congr_fun h v

private theorem divergence_of_constant_multiple {n : Nat} (c : Real)
    (F : Space n -> Space n) (x : Space n) :
    divergence (fun y i => c * F y i) x = c * divergence F x := by
  simp only [divergence, derivative_of_constant_multiple, Finset.mul_sum]

/-- Independently implemented direct inhabitant of the frozen target. -/
theorem independentRoot : Statement := by
  intro n _ rho heatCapacity conductivity _ _ _ temperature heatFlux source fluxLaw t x balance
  have hflux : heatFlux t = fun y i => -conductivity * gradient (temperature t) y i := by
    funext y
    exact fluxLaw t y
  rw [balance, hflux]
  simp only [divergence_of_constant_multiple, laplacian]
  ring

#print axioms independentRoot

end Stage1Instances.THM_M_1131.Validation
