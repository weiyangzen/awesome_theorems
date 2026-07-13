import Mathlib.LinearAlgebra.Matrix.PosDef
import Mathlib.LinearAlgebra.Matrix.ToLin

/-!
# THM-M-1455 discovery-only intake probe

These checks authenticate pinned positive-definite-matrix and matrix-vector interfaces adjacent to
a future conjugate-gradient encoding. They do not define the recurrence, select a source theorem,
construct an iteration, or prove the catalog claim.
-/

#check Matrix.PosDef
#check Matrix.PosDef.isHermitian
#check Matrix.posDef_iff_dotProduct_mulVec
#check Matrix.PosDef.dotProduct_mulVec_pos
#check Matrix.PosDef.isUnit
#check Matrix.mulVec
#check Matrix.mulVecLin
#check Matrix.mulVecLin_apply
#check Matrix.dotProduct_mulVec
#check dotProduct

#print axioms Matrix.PosDef.isUnit
#print axioms Matrix.posDef_iff_dotProduct_mulVec
