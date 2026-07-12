import Mathlib.Algebra.BrauerGroup.Defs

/-! Discovery-only checks for later source selection and exact statement work. -/

#check CSA
#check IsBrauerEquivalent
#check IsBrauerEquivalent.refl
#check IsBrauerEquivalent.symm
#check IsBrauerEquivalent.trans
#check IsBrauerEquivalent.is_eqv
#check Brauer.CSA_Setoid
#check BrauerGroup

#print axioms IsBrauerEquivalent.trans
#print axioms IsBrauerEquivalent.is_eqv
