import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Data.Finset.Interval
import Mathlib.Data.Nat.Sqrt

/-!
# THM-M-0956 discovery-only intake probe

These checks authenticate adjacent pinned finite-set, interval, pairwise, injectivity, sum, and
square-root APIs. They neither select an Erdos-Turan construction statement nor state or prove a
Sidon theorem.
-/

#check Finset
#check Finset.Icc
#check Finset.card
#check Finset.image
#check Set.Pairwise
#check Set.InjOn
#check Finset.sum
#check Nat.sqrt
