import Mathlib.LinearAlgebra.QuadraticForm.Signature
import Mathlib.LinearAlgebra.QuadraticForm.Real
import Mathlib.LinearAlgebra.Matrix.Symmetric

/-!
# THM-M-0050 discovery-only intake probe

These checks authenticate pinned signature, equivalence, real diagonalization, symmetric-matrix,
and matrix/quadratic-form transport APIs. They do not select the catalog's exact congruence or
inertia definitions, freeze a canonical target, prove the matrix transport, or establish theorem
completion.
-/

#check Matrix.IsSymm
#check Matrix.toQuadraticMap'
#check QuadraticMap.toMatrix'_comp
#check QuadraticMap.Equivalent
#check sigPos
#check sigNeg
#check QuadraticMap.Equivalent.sigPos_eq
#check QuadraticMap.Equivalent.sigNeg_eq
#check QuadraticForm.sigPos_of_equiv_weightedSumSquares
#check QuadraticForm.sigNeg_of_equiv_weightedSumSquares
#check QuadraticForm.equivalent_one_zero_neg_one_weighted_sum_squared
