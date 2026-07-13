import Mathlib.Analysis.InnerProductSpace.LaxMilgram
import Mathlib.Analysis.InnerProductSpace.Projection.Basic

/-!
# THM-M-1461 discovery-only intake probe

These checks authenticate pinned coercive-bilinear-form and orthogonal-projection interfaces that
could support a later source-selected variational finite-element statement. They do not define a
mesh, finite-element space, discrete PDE, canonical error theorem, or proof of THM-M-1461.
-/

#check IsCoercive.continuousLinearEquivOfBilin
#check IsCoercive.continuousLinearEquivOfBilin_apply
#check IsCoercive.unique_continuousLinearEquivOfBilin
#check Submodule.orthogonalProjection
#check Submodule.starProjection_inner_eq_zero
#check Submodule.eq_starProjection_of_mem_of_inner_eq_zero
#check Submodule.starProjection_minimal
#check Submodule.norm_orthogonalProjection_apply_le

#print axioms IsCoercive.unique_continuousLinearEquivOfBilin
#print axioms Submodule.starProjection_minimal
