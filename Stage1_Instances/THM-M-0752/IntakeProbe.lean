import Mathlib.Computability.TuringDegree

/-!
# THM-M-0752 discovery-only intake probe

These checks authenticate the pinned oracle-computability and Turing-degree vocabulary adjacent to
the catalog target. They do not define a jump, choose one property of it as the canonical theorem,
declare a wrapper, or prove THM-M-0752.
-/

namespace Stage1Instances.THM_M_0752

open scoped Computability

#check RecursiveIn
#check TuringReducible
#check TuringEquivalent
#check TuringReducible.refl
#check TuringReducible.trans
#check TuringEquivalent.equivalence
#check TuringDegree
#check TuringDegree.instPartialOrder

end Stage1Instances.THM_M_0752
