import Mathlib.Analysis.Calculus.FDeriv.Add

import Statement

/-!
# THM-M-1131 obligation interfaces and checked composition

This module checks the small algebraic architecture for the frozen target. The
final composition theorem remains conditional on the open divergence rewrite;
it is not a proof of `Statement`.
-/

noncomputable section

namespace Stage1Instances.THM_M_1131

/-- Output of the constitutive-law subtree at one fixed time. -/
def FluxDivergencePackage : Prop :=
  forall (n : Nat) (conductivity : Real)
      (temperature : Real -> Space n -> Real)
      (heatFlux : Real -> Space n -> Space n),
    (forall t x,
      heatFlux t x = fun i => -conductivity * gradient (temperature t) x i) ->
    forall t x,
      -divergence (heatFlux t) x = conductivity * laplacian (temperature t) x

/-- The energy balance and a fixed-time flux-divergence identity give the PDE. -/
theorem heatEquation_of_balance_of_fluxDivergence
    {n : Nat} {rho heatCapacity conductivity : Real}
    {temperature : Real -> Space n -> Real}
    {heatFlux : Real -> Space n -> Space n} {source : Real -> Space n -> Real}
    {t : Real} {x : Space n}
    (balance : rho * heatCapacity * timeDerivative temperature t x =
      -divergence (heatFlux t) x + source t x)
    (fluxDivergence : -divergence (heatFlux t) x =
      conductivity * laplacian (temperature t) x) :
    rho * heatCapacity * timeDerivative temperature t x =
      conductivity * laplacian (temperature t) x + source t x := by
  rw [balance, fluxDivergence]

/-- Exact root composition, conditional on the still-open constitutive subtree. -/
theorem statement_of_fluxDivergencePackage
    (fluxPackage : FluxDivergencePackage) : Statement := by
  intro n _ rho heatCapacity conductivity _ _ _ temperature heatFlux source fluxLaw t x balance
  exact heatEquation_of_balance_of_fluxDivergence balance
    (fluxPackage n conductivity temperature heatFlux fluxLaw t x)

#print axioms heatEquation_of_balance_of_fluxDivergence
#print axioms statement_of_fluxDivergencePackage

end Stage1Instances.THM_M_1131
