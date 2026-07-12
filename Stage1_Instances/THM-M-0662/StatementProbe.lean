import Mathlib.ModelTheory.Types

/-!
Pinned-environment substrate probe for the THM-M-0662 exact-statement blocker.

These declarations support first-order theories and complete types. They do not define simple
theories, a tree property, dividing or forking, or a classification theorem, so this file is not
the canonical target.
-/

#check FirstOrder.Language.Theory
#check FirstOrder.Language.Theory.IsComplete
#check FirstOrder.Language.Theory.IsSatisfiable
#check FirstOrder.Language.Formula
#check FirstOrder.Language.Theory.CompleteType
#check FirstOrder.Language.Theory.typeOf
