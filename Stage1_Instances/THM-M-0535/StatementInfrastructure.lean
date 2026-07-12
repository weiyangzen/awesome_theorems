import Mathlib.AlgebraicTopology.SingularHomology.Basic

/-!
Elaboration probe for the THM-M-0535 exact-statement blocker.

This checks only the pinned absolute singular-homology and ambient-topology
substrates. It deliberately defines no excision target: the repository record
does not select an exact source proposition, and pinned mathlib has no relative
singular-homology pair API from which to state its induced excision map.
-/

open Set

namespace Stage1Instances.THM_M_0535

universe u

#check AlgebraicTopology.singularChainComplexFunctor
#check AlgebraicTopology.singularHomologyFunctor

/-- The conventional ambient-set side condition can be expressed in the
pinned topology API. This is not the excision theorem. -/
def ConventionalExcisionCondition
    (X : Type u) [TopologicalSpace X] (A Z : Set X) : Prop :=
  closure Z ⊆ interior A

#check ConventionalExcisionCondition

end Stage1Instances.THM_M_0535
