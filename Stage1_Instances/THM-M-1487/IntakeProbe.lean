import Mathlib.Analysis.SpecialFunctions.Sigmoid
import Mathlib.Data.Holor
import Mathlib.Data.Matrix.Mul

/-!
# THM-M-1487 discovery-only intake probe

These checks authenticate adjacent pinned tensor, matrix, and activation-function APIs. They do
not define a convolutional neural network, select a source proposition, or prove THM-M-1487.
-/

#check Holor
#check Holor.slice
#check Holor.sum_unitVec_mul_slice
#check Holor.cprank_upper_bound
#check dotProduct
#check Matrix.mulVec
#check Matrix.mulVec_add
#check Real.sigmoid
#check Real.sigmoid_pos
#check Real.sigmoid_lt_one

#print axioms Holor.sum_unitVec_mul_slice
#print axioms Matrix.mulVec_add
#print axioms Real.sigmoid_lt_one
