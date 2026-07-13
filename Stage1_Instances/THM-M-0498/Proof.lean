import ObligationTree
import Mathlib.NumberTheory.LSeries.Dirichlet
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0498 partial proof execution

This module checks the intended frozen Dirichlet-series bridge using pinned
mathlib. Its frozen fingerprint is still planned, and the Perron, contour,
residue, and zero-sum obligations remain open, so this is not a proof of
`RiemannVonMangoldtTarget`.
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

assert_no_sorry ArithmeticFunction.LSeries_vonMangoldt_eq_deriv_riemannZeta_div
assert_no_sorry LSeries_vonMangoldt_logDerivative

#print sorries ArithmeticFunction.LSeries_vonMangoldt_eq_deriv_riemannZeta_div
#print sorries LSeries_vonMangoldt_logDerivative

#print axioms ArithmeticFunction.LSeries_vonMangoldt_eq_deriv_riemannZeta_div
#print axioms LSeries_vonMangoldt_logDerivative

end Stage1Instances.THM_M_0498
