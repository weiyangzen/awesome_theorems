import Mathlib.Analysis.InnerProductSpace.LaxMilgram
import Mathlib.Topology.MetricSpace.Contracting

/-!
# THM-M-1470 discovery-only intake probe

These checks authenticate pinned coercive-form, projection, and error-bound interfaces adjacent to
possible future numerical-analysis statements. The contraction theorem is deliberately checked as
a tempting name match that belongs to fixed-point iteration, not to Babuška's finite-element error
bound family. This file selects no PDE, discretization, estimator, reliability or efficiency claim,
and proves no theorem for THM-M-1470.
-/

#check IsCoercive.bounded_below
#check IsCoercive.continuousLinearEquivOfBilin
#check IsCoercive.continuousLinearEquivOfBilin_apply
#check Submodule.starProjection_inner_eq_zero
#check Submodule.starProjection_minimal
#check ContractingWith.aposteriori_dist_iterate_fixedPoint_le

#print axioms IsCoercive.bounded_below
#print axioms Submodule.starProjection_minimal
#print axioms ContractingWith.aposteriori_dist_iterate_fixedPoint_le
