import Mathlib.FieldTheory.IsRealClosed.Basic
import Mathlib.ModelTheory.Algebra.Ring.Basic
import Mathlib.ModelTheory.Complexity

/-! Checked interfaces found by the THM-M-0669 anchor audit. This file does
not state or prove quantifier elimination. -/

open FirstOrder FirstOrder.Language

#check IsRealClosed
#check IsRealClosed.isSquare_or_isSquare_neg
#check IsRealClosed.exists_isRoot_of_odd_natDegree
#check Language.ring
#check Language.BoundedFormula.IsQF
#check Language.Theory.Iff
#check Language.completeTheory
