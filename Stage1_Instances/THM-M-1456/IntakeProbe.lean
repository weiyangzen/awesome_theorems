import Mathlib.Analysis.Matrix.Normed
import Mathlib.Dynamics.FixedPoints.Topology
import Mathlib.LinearAlgebra.Matrix.NonsingularInverse
import Mathlib.LinearAlgebra.Matrix.PosDef

/-!
# THM-M-1456 discovery-only intake probe

These checks authenticate pinned matrix-inverse, positive-definite, norm, and fixed-point
interfaces adjacent to possible future preconditioning statements. They do not define a
preconditioner, select an iterative method or convergence comparison, or prove the catalog claim.
-/

#check Matrix.mulVec_mulVec
#check Matrix.mulVecLin_mul
#check Matrix.mul_inv_of_invertible
#check Matrix.inv_mul_of_invertible
#check Matrix.inv_mulVec_eq_vec
#check Matrix.mulVec_injective_of_invertible
#check Matrix.mulVec_surjective_of_invertible
#check Matrix.PosDef
#check Matrix.PosDef.isUnit
#check Matrix.PosDef.inv
#check Matrix.posDef_inv_iff
#check Matrix.linfty_opNorm_mul
#check Matrix.linfty_opNorm_mulVec
#check Function.IsFixedPt
#check isFixedPt_of_tendsto_iterate

#print axioms Matrix.inv_mulVec_eq_vec
#print axioms Matrix.PosDef.inv
#print axioms isFixedPt_of_tendsto_iterate
