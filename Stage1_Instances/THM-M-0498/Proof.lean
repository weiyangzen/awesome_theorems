import Mathlib.NumberTheory.LSeries.Dirichlet

/-!
# THM-M-0498 partial proof execution

This module closes the frozen Dirichlet-series bridge using pinned mathlib.
The Perron, contour, residue, and zero-sum obligations remain open, so this is
not a proof of `RiemannVonMangoldtTarget`.
-/

noncomputable section

open Complex

namespace Stage1Instances.THM_M_0498

/-- The von Mangoldt Dirichlet series is the negative logarithmic derivative
of the Riemann zeta function in its half-plane of absolute convergence. -/
theorem LSeries_vonMangoldt_logDerivative {s : Complex} (hs : 1 < s.re) :
    LSeries (fun n : Nat => ((ArithmeticFunction.vonMangoldt n : Real) : Complex)) s =
      -deriv riemannZeta s / riemannZeta s := by
  exact ArithmeticFunction.LSeries_vonMangoldt_eq_deriv_riemannZeta_div hs

#print axioms LSeries_vonMangoldt_logDerivative

end Stage1Instances.THM_M_0498
