import Mathlib.Analysis.InnerProductSpace.LaxMilgram
import Mathlib.Analysis.InnerProductSpace.Projection.Basic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Chebyshev.ChebyshevGauss
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Chebyshev.Orthogonality

/-!
# THM-M-1467 discovery-only intake probe

These checks authenticate pinned variational, projection, polynomial, orthogonality, and quadrature
interfaces adjacent to possible future spectral-element statements. They do not define an element
mesh, reference-to-physical maps, a conforming high-order space, a discrete PDE, or any canonical
solvability, stability, convergence, or error theorem for THM-M-1467.
-/

#check IsCoercive.continuousLinearEquivOfBilin
#check IsCoercive.unique_continuousLinearEquivOfBilin
#check Submodule.orthogonalProjection
#check Submodule.starProjection_minimal
#check Polynomial.Chebyshev.T
#check Polynomial.Chebyshev.integral_eval_T_real_mul_eval_T_real_measureT_of_ne
#check Polynomial.Chebyshev.sumZeroes
#check Polynomial.Chebyshev.integral_eq_sumZeroes

#print axioms IsCoercive.unique_continuousLinearEquivOfBilin
#print axioms Submodule.starProjection_minimal
#print axioms Polynomial.Chebyshev.integral_eq_sumZeroes
