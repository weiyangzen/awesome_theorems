import Mathlib.Computability.TuringDegree

/-!
Discovery-only checks for the pinned Turing-degree order interface.

This file deliberately declares no canonical target, join construction, wrapper theorem, or proof.
The repository source does not yet determine the exact supremum statement or encoding.
-/

namespace Stage1Instances.THM_M_0751

#check TuringReducible
#check TuringEquivalent
#check TuringDegree
#check TuringDegree.instPartialOrder

example : PartialOrder TuringDegree := TuringDegree.instPartialOrder

end Stage1Instances.THM_M_0751
