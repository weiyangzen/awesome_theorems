import Mathlib.Combinatorics.Additive.AP.Three.Defs
import Mathlib.Data.Fintype.Card
import Mathlib.Data.ZMod.Basic

/-!
# THM-M-0960 discovery-only intake probe

These checks authenticate pinned finite-vector-space, cardinality, and three-term-progression
interfaces adjacent to a future source-selected Ellenberg-Gijswijt target. This file states no
cap-set upper bound and supplies no proof credit.
-/

namespace Stage1Instances.THM_M_0960

/-- A prospective ambient space for the source's `q = 3` cap-set specialization. -/
abbrev CapAmbient (n : Nat) := Fin n -> ZMod 3

/-- A prospective cap-set predicate; the source-to-mathlib definition transport remains open. -/
def IsCapSet {n : Nat} (A : Set (CapAmbient n)) : Prop :=
  ThreeAPFree A

#check ZMod.card
#check Fintype.card_fun
#check ThreeAPFree
#check CapAmbient
#check IsCapSet
#check (Finset.univ : Finset (CapAmbient 2))
#check Finset.card_univ

end Stage1Instances.THM_M_0960
