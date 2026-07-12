import Mathlib.NumberTheory.Chebyshev
import Mathlib.NumberTheory.LSeries.Dirichlet
import Mathlib.NumberTheory.LSeries.RiemannZeta
import Mathlib.NumberTheory.EulerProduct.DirichletLSeries

/-!
# THM-M-0498: pinned mathlib anchor probes

These declarations are supporting infrastructure for the explicit formula.
None has the type of `RiemannVonMangoldtTarget`.
-/

#check Chebyshev.psi
#check Chebyshev.theta
#check ArithmeticFunction.vonMangoldt
#check Chebyshev.psi_eq_sum_theta
#check Chebyshev.primeCounting_eq_theta_div_log_add_integral
#check ArithmeticFunction.LSeries_vonMangoldt_eq_deriv_riemannZeta_div
#check riemannZeta_eulerProduct_exp_log
#check riemannZeta_residue_one
#check riemannZeta_neg_two_mul_nat_add_one
