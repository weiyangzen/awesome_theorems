import Mathlib.Analysis.Fourier.AddCircle
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Chebyshev.ChebyshevGauss
import Mathlib.Topology.ContinuousMap.Weierstrass

/-!
# THM-M-1460 discovery-only intake probe

These checks authenticate pinned orthogonal-polynomial, exact-quadrature, Fourier-basis, and
polynomial-approximation interfaces that could support a future spectral-method statement. They do
not select a differential equation, discretization, error theorem, or canonical THM-M-1460 target.
-/

#check Polynomial.Chebyshev.T
#check Polynomial.Chebyshev.chebyshevTsequence
#check Polynomial.Chebyshev.measureT
#check Polynomial.Chebyshev.integral_eval_T_real_mul_eval_T_real_measureT_of_ne
#check Polynomial.Chebyshev.sumZeroes
#check Polynomial.Chebyshev.integral_eq_sumZeroes
#check fourierBasis
#check hasSum_fourier_series_L2
#check exists_polynomial_near_continuousMap

#print axioms Polynomial.Chebyshev.integral_eq_sumZeroes
#print axioms hasSum_fourier_series_L2
#print axioms exists_polynomial_near_continuousMap
