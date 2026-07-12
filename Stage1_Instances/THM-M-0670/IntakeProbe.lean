import Mathlib.ModelTheory.Arithmetic.Presburger.Definability
import Mathlib.ModelTheory.Complexity

/- Discovery-only checks for ingredients of a later exact quantifier-elimination statement. -/
#check FirstOrder.Language.presburger
#check FirstOrder.Language.BoundedFormula
#check FirstOrder.Language.BoundedFormula.IsQF
#check FirstOrder.Language.BoundedFormula.Realize
#check FirstOrder.Language.Formula
#check FirstOrder.Language.Formula.Realize
#check FirstOrder.Language.presburger.definable_iff_isSemilinearSet
