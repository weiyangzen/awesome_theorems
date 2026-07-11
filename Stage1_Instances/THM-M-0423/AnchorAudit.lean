import Mathlib.LinearAlgebra.QuadraticForm.Basic
import Mathlib.LinearAlgebra.QuadraticForm.Radical
import Mathlib.LinearAlgebra.QuadraticForm.Real
import Mathlib.LinearAlgebra.QuadraticForm.TensorProduct
import Mathlib.NumberTheory.NumberField.Completion.FinitePlace
import Mathlib.NumberTheory.NumberField.Completion.InfinitePlace
import Mathlib.NumberTheory.NumberField.ProductFormula

/-!
# THM-M-0423 pinned anchor probes

These declarations are the usable Hasse-Minkowski substrate in the pinned
mathlib snapshot. None states the number-field local-global theorem frozen in
`Statement.lean`.
-/

namespace Stage1.THM_M_0423.AnchorAudit

def auditedMathlibRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

#check QuadraticMap.not_anisotropic_iff_exists
#check QuadraticMap.nondegenerate_iff_radical_eq_bot
#check QuadraticForm.baseChange
#check QuadraticForm.baseChange_tmul
#check QuadraticForm.equivalent_one_zero_neg_one_weighted_sum_squared
#check NumberField.FinitePlace
#check NumberField.InfinitePlace
#check NumberField.prod_abs_eq_one

end Stage1.THM_M_0423.AnchorAudit
