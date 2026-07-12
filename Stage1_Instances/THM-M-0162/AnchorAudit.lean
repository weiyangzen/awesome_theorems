import Mathlib.Analysis.InnerProductSpace.Calculus
import Mathlib.Geometry.Euclidean.Angle.Unoriented.CrossProduct
import Mathlib.LinearAlgebra.CrossProduct

/-!
# THM-M-0162 anchor-audit probes

This file checks the pinned mathlib interfaces identified by the anchor audit.
It deliberately states no Frenet-Serret theorem and imports no external candidate.
-/

open Matrix

#check crossProduct
#check dot_self_cross
#check dot_cross_self
#check triple_product_permutation
#check cross_dot_cross
#check cross_cross_eq_smul_sub_smul
#check HasDerivAt.inner
#check deriv_inner_apply
#check InnerProductGeometry.norm_toLp_symm_crossProduct
