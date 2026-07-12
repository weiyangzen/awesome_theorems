import Mathlib.FieldTheory.IsRealClosed.Basic
import Mathlib.ModelTheory.Algebra.Ring.Basic
import Mathlib.ModelTheory.Equivalence

/- Discovery-only checks for ingredients of a later exact Tarski statement. -/
#check IsRealClosed
#check FirstOrder.Language.ring
#check FirstOrder.Language.BoundedFormula
#check FirstOrder.Language.BoundedFormula.Realize
#check FirstOrder.Language.Theory.Iff
#check FirstOrder.Language.Theory.Model
