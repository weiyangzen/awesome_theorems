import Mathlib.Analysis.Convex.Jensen
import Mathlib.Analysis.MeanInequalities
import Mathlib.Analysis.Matrix.PosDef
import Mathlib.LinearAlgebra.Matrix.PosDef
import Mathlib.MeasureTheory.Function.Jacobian

/-!
# THM-M-1177 anchor audit

This file checks the pinned mathlib declarations that are plausible ingredients
of an ABP development. None has the type of the frozen ABP target.
-/

#check ConvexOn.exists_ge_of_mem_convexHull
#check Real.geom_mean_le_arith_mean
#check Matrix.posDef_iff_dotProduct_mulVec
#check Matrix.PosDef.det_pos
#check MeasureTheory.lintegral_abs_det_fderiv_eq_addHaar_image
#check MeasureTheory.lintegral_image_eq_lintegral_abs_det_fderiv_mul
#check MeasureTheory.integral_image_eq_integral_abs_det_fderiv_smul

#print axioms ConvexOn.exists_ge_of_mem_convexHull
#print axioms Real.geom_mean_le_arith_mean
#print axioms Matrix.PosDef.det_pos
#print axioms MeasureTheory.lintegral_abs_det_fderiv_eq_addHaar_image
