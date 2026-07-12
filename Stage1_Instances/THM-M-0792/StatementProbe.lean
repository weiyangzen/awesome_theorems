import Mathlib.ModelTheory.Semantics

/-!
This probe checks the nearest pinned first-order semantics substrate. It deliberately does not
define a forcing relation, forcing names, genericity, or a canonical theorem target: the repository
source has not fixed those notions or selected one exact proposition.
-/

open FirstOrder

#check FirstOrder.Language
#check FirstOrder.Language.Formula
#check FirstOrder.Language.Sentence
#check FirstOrder.Language.Formula.Realize
#check FirstOrder.Language.Sentence.Realize
#check FirstOrder.Language.Theory.Model
