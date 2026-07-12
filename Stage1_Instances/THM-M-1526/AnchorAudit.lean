import Mathlib.LinearAlgebra.CliffordAlgebra.Basic
import Mathlib.LinearAlgebra.Matrix.ToLin

/-!
# THM-M-1526: pinned anchor probes

These checks establish the nearby Clifford-algebra and matrix-to-operator API
in the pinned mathlib revision. None of them proves the frozen free Dirac
factorization target.
-/

#check CliffordAlgebra
#check CliffordAlgebra.ι
#check CliffordAlgebra.ι_sq_scalar
#check CliffordAlgebra.comp_ι_sq_scalar
#check CliffordAlgebra.lift
#check CliffordAlgebra.lift_ι_apply
#check CliffordAlgebra.ι_mul_ι_add_swap
#check Matrix.toLin
#check Matrix.toLin_one
#check Matrix.toLin_apply
#check Matrix.toLin_mul
#check Matrix.toLin_mul_apply
