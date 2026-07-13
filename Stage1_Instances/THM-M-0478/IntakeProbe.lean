import Mathlib.NumberTheory.LegendreSymbol.QuadraticReciprocity

/-!
# THM-M-0478 discovery-only intake probe

These checks authenticate the pinned Legendre-symbol definition and quadratic-reciprocity theorem
family. They do not select a canonical source statement, provide checked transports, audit terminal
proof provenance, or prove the repository target.
-/

#check legendreSym
#check legendreSym.quadratic_reciprocity
#check legendreSym.quadratic_reciprocity'
#check legendreSym.quadratic_reciprocity_one_mod_four
#check legendreSym.quadratic_reciprocity_three_mod_four
#check ZMod.exists_sq_eq_prime_iff_of_mod_four_eq_one
#check ZMod.exists_sq_eq_prime_iff_of_mod_four_eq_three
#print axioms legendreSym.quadratic_reciprocity
#print axioms legendreSym.quadratic_reciprocity'
