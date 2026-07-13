import Mathlib.Computability.ContextFreeGrammar

/-! Discovery-only API checks near a future exact CFL closure statement. -/

#check Language
#check Language.add_def
#check Language.mul_def
#check Language.kstar_def
#check Language.reverse
#check ContextFreeGrammar
#check ContextFreeGrammar.language
#check Language.IsContextFree
#check Language.IsContextFree.reverse
#print axioms Language.IsContextFree.reverse
