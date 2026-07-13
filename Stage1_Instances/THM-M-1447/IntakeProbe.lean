import Mathlib.Analysis.InnerProductSpace.GramMatrix
import Mathlib.Analysis.Matrix.LDL

/-!
# THM-M-1447 discovery-only intake probe

These checks authenticate pinned positive-definite-matrix, Gram-matrix, and adjacent LDL APIs. They
do not select or prove an exact real or complex Cholesky factor-existence or uniqueness theorem.
-/

#check Matrix.PosDef
#check Matrix.PosDef.isHermitian
#check Matrix.PosDef.diag_pos
#check Matrix.PosDef.isUnit
#check Matrix.posDef_iff_dotProduct_mulVec
#check Matrix.PosDef.conjTranspose_mul_self
#check Matrix.PosDef.mul_conjTranspose_self
#check Matrix.posDef_gram_iff_linearIndependent
#check LDL.lower
#check LDL.diag
#check LDL.lowerInv_triangular
#check LDL.lower_conj_diag

namespace THMM1447Intake

/- A checked statement of the adjacent pinned LDL result. The factor `L` is not asserted lower
triangular here, `D` is not absorbed by square roots, and this is not the Cholesky target. -/
theorem posDef_exists_ldl {d : ℕ} {S : Matrix (Fin d) (Fin d) ℝ} (hS : S.PosDef) :
    ∃ L D : Matrix (Fin d) (Fin d) ℝ,
      (∀ i j, i ≠ j → D i j = 0) ∧ L * D * L.transpose = S := by
  refine ⟨LDL.lower hS, LDL.diag hS, ?_, ?_⟩
  · intro i j hij
    simp [LDL.diag, hij]
  · simpa using LDL.lower_conj_diag hS

#print axioms THMM1447Intake.posDef_exists_ldl

end THMM1447Intake
