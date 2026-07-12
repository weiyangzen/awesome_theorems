import Mathlib.LinearAlgebra.Eigenspace.Triangularizable
import Mathlib.LinearAlgebra.JordanChevalley
import Mathlib.LinearAlgebra.Matrix.GeneralLinearGroup.Defs

/-!
# THM-M-0042 discovery-only intake probe

These checks authenticate pinned generalized-eigenspace, Jordan-Chevalley, invertible-matrix,
change-of-basis, matrix-representation, and block-matrix APIs. They do not define Jordan blocks,
select a canonical target, or prove the Jordan canonical form theorem.
-/

#check Module.End.iSup_maxGenEigenspace_eq_top
#check Module.End.exists_isNilpotent_isSemisimple
#check Matrix.GeneralLinearGroup
#check Matrix.GeneralLinearGroup.toLin
#check LinearMap.toMatrix
#check Module.Basis.toMatrix
#check Matrix.diagonal
#check Matrix.fromBlocks
