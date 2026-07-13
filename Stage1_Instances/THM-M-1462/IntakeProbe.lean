import Mathlib.Analysis.InnerProductSpace.LaxMilgram
import Mathlib.Analysis.InnerProductSpace.Projection.FiniteDimensional

/-!
# THM-M-1462 discovery-only intake probe

These checks authenticate pinned coercive-form and orthogonal-projection APIs adjacent to possible
Galerkin statements. They do not select a statement, define a Galerkin discretization, or prove
THM-M-1462.
-/

#check IsCoercive
#check IsCoercive.continuousLinearEquivOfBilin
#check IsCoercive.continuousLinearEquivOfBilin_apply
#check IsCoercive.unique_continuousLinearEquivOfBilin
#check Submodule.HasOrthogonalProjection
#check Submodule.orthogonalProjection
#check Submodule.orthogonalProjectionFn_inner_eq_zero
#check Submodule.eq_orthogonalProjectionFn_of_mem_of_inner_eq_zero
#check Submodule.starProjection_minimal
#check Submodule.orthogonalProjection_mem_subspace_eq_self
