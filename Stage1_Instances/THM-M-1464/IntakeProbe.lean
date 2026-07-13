import Mathlib.Analysis.InnerProductSpace.LaxMilgram
import Mathlib.Geometry.Euclidean.Simplex
import Mathlib.MeasureTheory.Integral.Bochner.Set

/-!
# THM-M-1464 discovery-only intake probe

These checks authenticate pinned affine-simplex, piecewise-integration, and coercive-bilinear-form
interfaces. They do not define a DG mesh or scheme, select a source proposition, or prove a
Reed-Hill construction, stability, convergence, error, or complexity theorem.
-/

#check Affine.Simplex
#check Affine.Triangle
#check Affine.Simplex.faceOpposite
#check Affine.Simplex.range_faceOpposite_points
#check MeasureTheory.integral_piecewise
#check IsCoercive
#check IsCoercive.continuousLinearEquivOfBilin
#check IsCoercive.continuousLinearEquivOfBilin_apply
#check IsCoercive.unique_continuousLinearEquivOfBilin

#print axioms Affine.Simplex.range_faceOpposite_points
#print axioms MeasureTheory.integral_piecewise
#print axioms IsCoercive.continuousLinearEquivOfBilin_apply
