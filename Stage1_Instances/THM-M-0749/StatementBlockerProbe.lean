import Mathlib.Computability.TuringDegree
import Mathlib.Computability.Halting

/-!
# THM-M-0749 statement-blocker probe

This file checks why the positive-information partial oracle from `IntakeProbe.lean` cannot be
used as the canonical set oracle for Friedberg-Muchnik. It does not select a replacement encoding,
state the canonical theorem, or prove incomparable computably enumerable Turing degrees.
-/

namespace Stage1Instances.THM_M_0749.StatementBlocker

open scoped Computability

/-- The discovery-only positive-information representation used by the intake probe. -/
def predicatePartialOracle (A : Nat -> Prop) : Nat -> Part Nat :=
  fun n => Part.assert (A n) fun _ => Part.some n

/-- A c.e. predicate makes the intake probe's positive-information representation partial
recursive. This is precisely why it cannot represent the ordinary Turing degree of a c.e. set. -/
theorem predicatePartialOracle_partrec {A : Nat -> Prop} (hA : REPred A) :
    Nat.Partrec (predicatePartialOracle A) := by
  apply Partrec.nat_iff.mp
  apply Partrec.of_eq
    (Partrec.map hA (Computable.fst (α := Nat) (β := Unit)).to₂)
  intro n
  apply Part.ext
  intro x
  simp [predicatePartialOracle, eq_comm]

/-- Consequently this representation of a c.e. predicate is reducible to every oracle. -/
theorem predicatePartialOracle_turingReducible {A B : Nat -> Prop} (hA : REPred A) :
    TuringReducible (predicatePartialOracle A) (predicatePartialOracle B) :=
  (predicatePartialOracle_partrec hA).turingReducible

/-- The prospective incomparability shape from the intake probe is inconsistent with its c.e.
hypotheses. A later statement phase must select and justify a genuine total set-oracle encoding. -/
theorem prospectiveIncomparability_impossible :
    Not (Exists fun A : Nat -> Prop => Exists fun B : Nat -> Prop =>
      REPred A /\ REPred B /\
        Not (TuringReducible (predicatePartialOracle A) (predicatePartialOracle B)) /\
        Not (TuringReducible (predicatePartialOracle B) (predicatePartialOracle A))) := by
  rintro ⟨A, B, hA, _hB, hAB, _hBA⟩
  exact hAB (predicatePartialOracle_turingReducible hA)

#check predicatePartialOracle_partrec
#check predicatePartialOracle_turingReducible
#check prospectiveIncomparability_impossible

end Stage1Instances.THM_M_0749.StatementBlocker
