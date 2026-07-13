import Mathlib.Analysis.InnerProductSpace.LaxMilgram
import Mathlib.Analysis.InnerProductSpace.Projection.Basic
import Mathlib.Analysis.Normed.Operator.Bilinear

/-!
# THM-M-1463 discovery-only intake probe

These checks authenticate pinned continuous bilinear-map, subspace, projection, and Lax-Milgram
interfaces adjacent to possible future Petrov-Galerkin statements. They do not select trial and
test spaces, define an inf-sup condition, or prove solvability, stability, quasi-optimality, or
convergence for the catalog target.
-/

#check ContinuousLinearMap
#check ContinuousLinearMap.opNorm_le_bound₂
#check ContinuousLinearMap.le_opNorm₂
#check Submodule.subtypeL
#check Submodule.orthogonalProjection
#check Submodule.orthogonalProjection_mem_subspace_eq_self
#check IsCoercive
#check IsCoercive.continuousLinearEquivOfBilin
#check IsCoercive.continuousLinearEquivOfBilin_apply
#check IsCoercive.unique_continuousLinearEquivOfBilin

#print axioms ContinuousLinearMap.le_opNorm₂
#print axioms Submodule.orthogonalProjection_mem_subspace_eq_self
#print axioms IsCoercive.continuousLinearEquivOfBilin_apply
