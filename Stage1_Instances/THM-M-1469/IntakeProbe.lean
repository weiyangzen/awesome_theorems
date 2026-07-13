import Mathlib.Analysis.InnerProductSpace.LaxMilgram
import Mathlib.Analysis.InnerProductSpace.Projection.FiniteDimensional
import Mathlib.Analysis.InnerProductSpace.Projection.Submodule

/-!
# THM-M-1469 discovery-only intake probe

These checks authenticate pinned coercive-form, projection, and nested-approximation interfaces
adjacent to possible adaptive finite-element statements. They do not define a mesh, estimator,
marking/refinement algorithm, canonical target, or proof of THM-M-1469.
-/

#check IsCoercive
#check IsCoercive.continuousLinearEquivOfBilin
#check IsCoercive.continuousLinearEquivOfBilin_apply
#check IsCoercive.unique_continuousLinearEquivOfBilin
#check Submodule.HasOrthogonalProjection
#check Submodule.orthogonalProjection
#check Submodule.orthogonalProjectionFn_inner_eq_zero
#check Submodule.starProjection_minimal
#check Submodule.orthogonalProjection_mem_subspace_eq_self
#check Submodule.starProjection_tendsto_closure_iSup
#check Submodule.starProjection_tendsto_self

#print axioms IsCoercive.unique_continuousLinearEquivOfBilin
#print axioms Submodule.starProjection_minimal
#print axioms Submodule.starProjection_tendsto_self
