import Mathlib.Computability.TuringDegree
import Mathlib.Computability.Halting

/-!
Discovery-only checks for pinned computability interfaces adjacent to the Friedberg-Muchnik
target. They neither define the canonical set-to-oracle transport nor prove incomparable c.e.
degrees.
-/

open scoped Computability

#check REPred
#check RecursiveIn
#check TuringReducible
#check TuringEquivalent
#check TuringDegree
#check TuringDegree.instPartialOrder

-- Prospective representation shape only; not the source-identical canonical target.
def predicatePartialOracle (A : Nat -> Prop) : Nat -> Part Nat :=
  fun n => Part.assert (A n) fun _ => Part.some n

#check (fun A B : Nat -> Prop =>
  REPred A /\ REPred B /\
    (Not (TuringReducible (predicatePartialOracle A) (predicatePartialOracle B))) /\
    (Not (TuringReducible (predicatePartialOracle B) (predicatePartialOracle A))))
