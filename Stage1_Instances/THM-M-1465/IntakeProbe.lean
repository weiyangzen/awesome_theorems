import Mathlib.Algebra.Group.ForwardDiff
import Mathlib.Analysis.Calculus.Taylor
import Mathlib.Analysis.InnerProductSpace.Laplacian

/-!
# THM-M-1465 discovery-only intake probe

These checks authenticate pinned algebraic forward-difference, continuous Laplacian, and Taylor-
remainder interfaces adjacent to the catalog topic. They do not define a finite-difference PDE
scheme, select a source proposition, or prove consistency, stability, convergence, solvability, or
an error estimate.
-/

#check fwdDiff
#check fwdDiff_iter_eq_sum_shift
#check shift_eq_sum_fwdDiff_iter
#check Laplacian.laplacian
#check InnerProductSpace.laplacianWithin
#check InnerProductSpace.laplacian_eq_iteratedFDeriv_orthonormalBasis
#check InnerProductSpace.laplacian_eq_iteratedDeriv_real
#check exists_taylor_mean_remainder_bound

#print axioms fwdDiff_iter_eq_sum_shift
#print axioms InnerProductSpace.laplacian_eq_iteratedDeriv_real
#print axioms exists_taylor_mean_remainder_bound
