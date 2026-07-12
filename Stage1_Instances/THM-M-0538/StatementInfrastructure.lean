import Mathlib.AlgebraicTopology.SingularHomology.Basic

/-!
Elaboration probe for the THM-M-0538 exact-statement blocker.

This file checks only the pinned absolute singular-homology substrate and one
dimension-like result. It deliberately does not define an Eilenberg-Steenrod
axiom package: the repository source does not choose a proposition, and this
import does not provide the required topological-pair and boundary-map API.
-/

namespace Stage1Instances.THM_M_0538

#check AlgebraicTopology.singularChainComplexFunctor
#check AlgebraicTopology.singularHomologyFunctor
#check AlgebraicTopology.isZero_singularHomologyFunctor_of_totallyDisconnectedSpace
#check AlgebraicTopology.singularHomologyFunctorZeroOfTotallyDisconnectedSpace

end Stage1Instances.THM_M_0538
