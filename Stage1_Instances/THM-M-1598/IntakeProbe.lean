import Mathlib.GroupTheory.SpecificGroups.Cyclic.Basic

/-!
# THM-M-1598 discovery-only intake probe

These checks authenticate pinned cyclic-group and repeated-exponentiation APIs adjacent to one
possible algebraic encoding of Diffie-Hellman. They do not select the catalog's exact statement,
define a key-agreement protocol or security game, or prove THM-M-1598.
-/

#check IsCyclic
#check IsCyclic.exists_generator
#check Subgroup.zpowers
#check pow_mul
#check pow_mul'
#check pow_mul_comm
#check orderOf
#check pow_orderOf_eq_one
