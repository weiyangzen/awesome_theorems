import Mathlib.FieldTheory.AbelRuffini

/-!
# THM-M-0064 discovery-only intake probe

These checks authenticate pinned solvability-by-radicals and nonsolvable-symmetric-group APIs.
They do not define the catalog's word "general", select a canonical polynomial target, construct a
generic polynomial with symmetric Galois group, or prove the degree-at-least-five root claim.
-/

#check solvableByRad
#check isSolvable_gal_minpoly
#check isSolvable_gal_of_irreducible
#check Equiv.Perm.fin_5_not_solvable
#check Equiv.Perm.not_solvable

#print axioms isSolvable_gal_of_irreducible
#print axioms Equiv.Perm.fin_5_not_solvable
