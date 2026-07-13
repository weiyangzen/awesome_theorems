import Mathlib.Combinatorics.SetFamily.Intersecting
import Mathlib.Combinatorics.SetFamily.KruskalKatona
import Mathlib.Data.Finset.Slice

/-!
Discovery-only substrate checks for a later source-selected Complete Intersection target.

This file states no target theorem. In particular, `Finset.erdos_ko_rado` is only the ordinary
`t = 1` upper bound and receives no proof credit for `THM-M-0965`.
-/

namespace Stage1Instances.THM_M_0965

/-- Prospective vocabulary only: pairwise intersections of distinct members have size at least `t`. -/
def IsTIntersecting {alpha : Type*} [DecidableEq alpha]
    (t : Nat) (family : Set (Finset alpha)) : Prop :=
  family.Pairwise fun A B => t <= (A ∩ B).card

#check Set.IsIntersectingOf
#check Set.Intersecting
#check Set.Sized
#check Finset.powersetCard
#check Finset.card_powersetCard
#check Nat.choose
#check Finset.erdos_ko_rado
#check IsTIntersecting

end Stage1Instances.THM_M_0965
