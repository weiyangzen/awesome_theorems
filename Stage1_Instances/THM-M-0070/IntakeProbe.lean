import Mathlib.Algebra.Group.PUnit
import Mathlib.GroupTheory.Solvable
import Mathlib.SetTheory.Cardinal.Finite

-- This probe checks only that the vocabulary needed to state the target is available.
#check IsSolvable
#check isSolvable_def
#check derivedSeries
#check CommGroup.isSolvable

universe u

example {G : Type u} [Group G] [Finite G] : Prop :=
  Odd (Nat.card G) -> IsSolvable G

-- The order-one boundary belongs to the source statement.
example : Prop := Odd (Nat.card (PUnit : Type)) ∧ IsSolvable (PUnit : Type)

#print axioms CommGroup.isSolvable
