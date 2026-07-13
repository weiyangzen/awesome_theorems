import Mathlib.Computability.TuringDegree

/-!
Discovery-only checks for the pinned Turing-degree substrate adjacent to jump inversion.

This file deliberately declares no jump operator, canonical target, or wrapper theorem. The
repository source does not yet determine the exact jump-inversion proposition.
-/

namespace Stage1Instances.THM_M_0753

#check RecursiveIn
#check TuringReducible
#check TuringEquivalent
#check TuringDegree
#check TuringDegree.instPartialOrder
#check TuringReducible.refl
#check TuringReducible.trans

end Stage1Instances.THM_M_0753
