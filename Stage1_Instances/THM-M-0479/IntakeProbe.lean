import Mathlib.NumberTheory.LSeries.PrimesInAP

/-!
# THM-M-0479 discovery-only intake probe

These checks authenticate pinned mathlib's direct Dirichlet-theorem interfaces and the residue-
class vocabulary needed to compare them. They do not freeze the catalog's canonical statement,
audit a terminal proof body, or supply proof credit.
-/

#check Nat.Prime
#check Nat.Coprime
#check Nat.ModEq
#check ZMod
#check IsUnit
#check Nat.infinite_setOf_prime_and_eq_mod
#check Nat.forall_exists_prime_gt_and_eq_mod
#check Nat.forall_exists_prime_gt_and_zmodEq
#check Nat.forall_exists_prime_gt_and_modEq
#check Nat.frequently_atTop_prime_and_modEq
#check Nat.infinite_setOf_prime_and_modEq

#print axioms Nat.infinite_setOf_prime_and_eq_mod
#print axioms Nat.infinite_setOf_prime_and_modEq
