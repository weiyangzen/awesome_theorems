import Mathlib.Computability.Halting

/-!
# THM-M-0708: exact Rice-theorem statement

This module freezes and tests the statement boundary only. It contains no new
proof of Rice's theorem.
-/

namespace Stage1Instances.THM_M_0708

open Nat.Partrec (Code)
open Nat.Partrec.Code

/-- The exact functional form of Rice's theorem selected at intake. A semantic
class is nontrivial when it contains one partial-recursive function and omits
another. Its induced predicate on program codes cannot be computable. -/
def RiceTheoremTarget : Prop :=
  forall C : Set (Nat →. Nat),
    (exists f : Nat →. Nat, Nat.Partrec f /\ f ∈ C) ->
    (exists g : Nat →. Nat, Nat.Partrec g /\ g ∉ C) ->
    Not (ComputablePred fun c : Code => eval c ∈ C)

/-- Direct predicate-style expansion of the intake claim. -/
def IntakePredicateShape : Prop :=
  forall S : (Nat →. Nat) -> Prop,
    (exists f : Nat →. Nat, Nat.Partrec f /\ S f) ->
    (exists g : Nat →. Nat, Nat.Partrec g /\ Not (S g)) ->
    Not (ComputablePred fun c : Code => S (eval c))

/-- Membership in a set and application of its characteristic predicate are
definitionally interchangeable; this checks the intake-to-target transport. -/
theorem riceTheoremTarget_iff_intakePredicateShape :
    RiceTheoremTarget <-> IntakePredicateShape := by
  rfl

-- Separately elaborated structural mutations used by `check_statement.py`.
def mutationRemovedNegativeWitness : Prop :=
  forall C : Set (Nat →. Nat),
    (exists f : Nat →. Nat, Nat.Partrec f /\ f ∈ C) ->
    Not (ComputablePred fun c : Code => eval c ∈ C)

def mutationRemovedPositiveWitness : Prop :=
  forall C : Set (Nat →. Nat),
    (exists g : Nat →. Nat, Nat.Partrec g /\ g ∉ C) ->
    Not (ComputablePred fun c : Code => eval c ∈ C)

def mutationIntensionalCodeProperty : Prop :=
  forall C : Set Code,
    C.Nonempty ->
    (Set.univ \ C).Nonempty ->
    Not (ComputablePred fun c : Code => c ∈ C)

def mutationTotalFunctionDomain : Prop :=
  forall C : Set (Nat -> Nat),
    C.Nonempty ->
    (Set.univ \ C).Nonempty ->
    Not (ComputablePred fun _c : Code => (fun n => n) ∈ C)

/-- The empty semantic class has a constant computable index predicate, so it
must be excluded by the positive witness premise. -/
theorem empty_property_is_computable :
    ComputablePred fun c : Code => eval c ∈ (∅ : Set (Nat →. Nat)) := by
  apply ComputablePred.of_eq
    (show ComputablePred (fun _c : Code => False) from
      ⟨fun _ => isFalse id, by simpa using (Computable.const (α := Code) false)⟩)
  intro c
  constructor
  · intro h
    exact False.elim h
  · intro h
    exact h

/-- The universal semantic class likewise has a constant computable index
predicate, so it must be excluded by the negative witness premise. -/
theorem universal_property_is_computable :
    ComputablePred fun c : Code => eval c ∈ (Set.univ : Set (Nat →. Nat)) := by
  apply ComputablePred.of_eq
    (show ComputablePred (fun _c : Code => True) from
      ⟨fun _ => isTrue trivial, by simpa using (Computable.const (α := Code) true)⟩)
  simp

end Stage1Instances.THM_M_0708

set_option pp.explicit true in
#print Stage1Instances.THM_M_0708.RiceTheoremTarget
