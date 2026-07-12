import Mathlib.LinearAlgebra.Matrix.Block
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.LinearAlgebra.Matrix.Transvection

/-!
# THM-M-0047 discovery and literal-scope probe

The theorem below checks that the catalog's unqualified universal unpivoted reading is false.
The remaining checks authenticate adjacent pinned triangular and pivot APIs. This file does not
select or prove a corrected LU theorem and gives no proof credit to the catalog target.
-/

open Matrix

def thmM0047SwapMatrix : Matrix (Fin 2) (Fin 2) ℚ :=
  !![0, 1; 1, 0]

theorem thmM0047_swap_not_lower_mul_upper :
    ¬ ∃ L U : Matrix (Fin 2) (Fin 2) ℚ,
      L.BlockTriangular OrderDual.toDual ∧
      U.BlockTriangular id ∧
      thmM0047SwapMatrix = L * U := by
  rintro ⟨L, U, hL, hU, hEq⟩
  have hL01 : L 0 1 = 0 := hL (by decide)
  have hU10 : U 1 0 = 0 := hU (by decide)
  have h00 := congrFun (congrFun hEq 0) 0
  have h01 := congrFun (congrFun hEq 0) 1
  have h10 := congrFun (congrFun hEq 1) 0
  simp [thmM0047SwapMatrix, Matrix.mul_apply, hL01, hU10] at h00 h01 h10
  rcases h00 with h | h
  · rw [h] at h01
    norm_num at h01
  · rw [h] at h10
    norm_num at h10

#check Matrix.BlockTriangular
#check Matrix.BlockTriangular.mul
#check Matrix.det_of_upperTriangular
#check Matrix.det_of_lowerTriangular
#check Matrix.mul_fin_two
#check Matrix.Pivot.exists_list_transvec_mul_diagonal_mul_list_transvec

#print axioms thmM0047_swap_not_lower_mul_upper
