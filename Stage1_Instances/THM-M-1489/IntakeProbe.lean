import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Data.Matrix.Mul
import Mathlib.Data.Real.Sqrt

/-!
# THM-M-1489 discovery-only intake probe

These checks authenticate generic pinned real exponential, square-root, finite matrix, and
matrix-vector interfaces adjacent to possible attention encodings. They do not define softmax,
scaled dot-product attention, a Transformer, a canonical target, or a proof of THM-M-1489.
-/

#check Real.exp
#check Real.exp_pos
#check Real.sqrt
#check Real.sqrt_pos
#check dotProduct
#check Matrix.transpose
#check Matrix.mul_apply
#check Matrix.mulVec
#check Matrix.mulVecLin
#check Matrix.mulVecLin_mul

#print axioms Real.exp_pos
#print axioms Real.sqrt_pos
#print axioms Matrix.mulVecLin_mul
