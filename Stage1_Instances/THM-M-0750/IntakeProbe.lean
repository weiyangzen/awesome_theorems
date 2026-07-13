import Mathlib.Computability.TuringDegree

/-!
# THM-M-0750 discovery-only intake probe

These checks authenticate the pinned oracle-reducibility and Turing-degree interfaces adjacent to
the catalog topic. They do not select one structural result, state a canonical THM-M-0750 theorem,
or transfer proof credit from mathlib.
-/

namespace Stage1Instances.THM_M_0750

#check RecursiveIn
#check TuringReducible
#check TuringEquivalent
#check TuringReducible.refl
#check TuringReducible.trans
#check TuringEquivalent.equivalence
#check TuringDegree
#check TuringDegree.instPartialOrder

#print axioms TuringReducible.trans
#print axioms TuringEquivalent.equivalence

end Stage1Instances.THM_M_0750
