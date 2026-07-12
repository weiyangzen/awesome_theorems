import Mathlib.Analysis.Calculus.FDeriv.Add

import ObligationTree

/-!
# THM-M-1131 proof

The proof is purely algebraic.  Mathlib's total Frechet derivative commutes
with multiplication by an arbitrary real scalar, including zero.  Applying
that identity coordinatewise rewrites the divergence of Fourier's flux, and
the checked composition theorem supplies the energy-balance conclusion.
-/

noncomputable section

namespace Stage1Instances.THM_M_1131

/-- A constant scalar passes through each coordinate derivative. -/
theorem fderiv_const_mul_apply {n : Nat} (c : Real) (f : Space n -> Real)
    (x v : Space n) :
    fderiv Real (fun y => c * f y) x v = c * fderiv Real f x v := by
  have h := congrFun (fderiv_const_smul_field (𝕜 := Real) (f := f) c) x
  simpa [Pi.smul_apply] using DFunLike.congr_fun h v

/-- Divergence of a constant scalar multiple is the same multiple of divergence. -/
theorem divergence_const_mul {n : Nat} (c : Real) (F : Space n -> Space n)
    (x : Space n) :
    divergence (fun y i => c * F y i) x = c * divergence F x := by
  simp only [divergence, fderiv_const_mul_apply, Finset.mul_sum]

/-- Fourier's constitutive equation gives the required flux-divergence identity. -/
theorem fluxDivergencePackage : FluxDivergencePackage := by
  intro n conductivity temperature heatFlux fluxLaw t x
  have hflux : heatFlux t = fun y i => -conductivity * gradient (temperature t) y i := by
    funext y
    exact fluxLaw t y
  rw [hflux]
  simp only [divergence_const_mul, laplacian]
  ring

/-- Exact kernel-checked proof of the frozen canonical target. -/
theorem fourierHeatConductionLaw : Statement :=
  statement_of_fluxDivergencePackage fluxDivergencePackage

#print axioms fderiv_const_mul_apply
#print axioms divergence_const_mul
#print axioms fluxDivergencePackage
#print axioms fourierHeatConductionLaw

end Stage1Instances.THM_M_1131
