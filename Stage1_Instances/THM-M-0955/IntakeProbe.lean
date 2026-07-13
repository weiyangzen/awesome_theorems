import Mathlib.Combinatorics.Additive.Energy
import Mathlib.Combinatorics.Additive.FreimanHom
import Mathlib.FieldTheory.Finite.Basic
import Mathlib.GroupTheory.SpecificGroups.Cyclic

/-!
# THM-M-0955 discovery-only intake probe

These checks authenticate adjacent pinned APIs for a possible finite-additive-group and finite-field
encoding of a Bose-Chowla construction. They do not define a Sidon or B_h predicate, select a
canonical proposition, construct the requested set, or prove THM-M-0955.
-/

#check IsAddFreimanHom
#check isAddFreimanHom_two
#check Finset.addEnergy
#check FiniteField.card
#check Fintype.card_units
#check IsCyclic.exists_generator
