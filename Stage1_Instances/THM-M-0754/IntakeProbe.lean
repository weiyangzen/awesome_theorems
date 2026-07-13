import Mathlib.Computability.Halting
import Mathlib.ModelTheory.Complexity

/-!
Discovery-only checks for pinned APIs adjacent to the arithmetical-hierarchy topic. No declaration
below defines, freezes, or proves a source-identical hierarchy theorem.
-/

open FirstOrder Nat.Partrec

#check FirstOrder.Language.BoundedFormula
#check FirstOrder.Language.BoundedFormula.IsQF
#check FirstOrder.Language.BoundedFormula.IsPrenex
#check FirstOrder.Language.BoundedFormula.IsUniversal
#check FirstOrder.Language.BoundedFormula.IsExistential
#check FirstOrder.Language.BoundedFormula.toPrenex
#check FirstOrder.Language.BoundedFormula.realize_toPrenex
#check PrimrecPred
#check ComputablePred
#check REPred
