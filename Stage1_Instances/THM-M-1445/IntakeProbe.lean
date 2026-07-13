import Mathlib.LinearAlgebra.Matrix.NonsingularInverse
import Mathlib.LinearAlgebra.Matrix.Transvection
import Mathlib.Tactic.Linarith.Oracle.SimplexAlgorithm.Gauss

/-!
# THM-M-1445 discovery-only intake probe

These checks authenticate pinned exact-arithmetic matrix reduction, row-operation,
matrix-vector, and Gaussian-elimination implementation surfaces. They do not select
a canonical correctness theorem or prove that the catalog's method label is a Prop.
-/

#check Matrix.transvection
#check Matrix.transvection_mul_apply_same
#check Matrix.det_transvection_of_ne
#check Matrix.Pivot.exists_list_transvec_mul_mul_list_transvec_eq_diagonal
#check Matrix.Pivot.exists_list_transvec_mul_diagonal_mul_list_transvec
#check Matrix.mulVecLin_mul
#check Matrix.inv_mulVec_eq_vec
#check Mathlib.Tactic.Linarith.SimplexAlgorithm.Gauss.getTableau
