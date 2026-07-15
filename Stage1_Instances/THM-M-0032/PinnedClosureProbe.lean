import Mathlib.RingTheory.RegularLocalRing.Defs

/-!
# THM-M-0032 pinned-closure proof probe

This negative fixture checks the two immediate typeclass obligations that a proof of the exact
target would have to discharge in the pinned Lean/mathlib closure. Both failures are intentional:
they keep the missing domain and UFD bodies visible without adding an unchecked assumption or
weakening the target.
-/

namespace Stage1Instances.THM_M_0032_PinnedClosureProbe

universe u

variable (R : Type u) [CommRing R] [IsRegularLocalRing R]

#check_failure (inferInstance : IsDomain R)
#check_failure (inferInstance : UniqueFactorizationMonoid R)

def ExactTarget : Prop :=
  forall (S : Type u) [CommRing S] [IsRegularLocalRing S],
    UniqueFactorizationMonoid S

set_option pp.universes true in
set_option pp.explicit true in
#print ExactTarget

end Stage1Instances.THM_M_0032_PinnedClosureProbe
