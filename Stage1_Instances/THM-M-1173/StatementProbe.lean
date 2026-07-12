import Mathlib.Topology.MetricSpace.Holder

/-!
Elaboration probe for the THM-M-1173 exact-statement blocker.

This file checks only the pinned mathlib conclusion-side Holder API. It does
not define a De Giorgi-Nash target: the repository source does not determine
the equation, weak-solution predicate, or quantitative regularity statement.
-/

#check HolderOnWith
#check HolderOnWith.continuousOn
