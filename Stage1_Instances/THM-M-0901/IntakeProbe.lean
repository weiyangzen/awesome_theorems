import Mathlib.Data.Fintype.BigOperators
import Mathlib.Data.Fintype.EquivFin
import Mathlib.Data.Matrix.Basic

/-!
# THM-M-0901 discovery-only intake probe

These checks authenticate pinned matrix, finite-cardinality, and bijection interfaces adjacent to a
future source-selected Latin-square encoding. They do not define a Latin predicate, select an
existence or counting theorem, or prove THM-M-0901.
-/

#check Matrix
#check Matrix.of
#check Fin
#check Fintype.card
#check Fintype.card_fun
#check Fintype.equivFin
#check Function.Bijective
#check Equiv.ofBijective
#check (Matrix (Fin 3) (Fin 3) (Fin 3))
