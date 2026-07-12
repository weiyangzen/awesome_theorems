import Mathlib.Computability.Halting

/-!
# THM-M-0708 independent validation probe

This module deliberately imports neither `Proof` nor `ObligationTree`. It
reconstructs the frozen target and closes it directly with the pinned mathlib
Rice theorem, providing a differential check of the proof-phase composition.
-/

namespace Stage1Instances.THM_M_0708.Validation

open Nat.Partrec (Code)
open Nat.Partrec.Code

def RiceTheoremTarget : Prop :=
  forall C : Set (Nat →. Nat),
    (exists f : Nat →. Nat, Nat.Partrec f /\ f ∈ C) ->
    (exists g : Nat →. Nat, Nat.Partrec g /\ g ∉ C) ->
    Not (ComputablePred fun c : Code => eval c ∈ C)

theorem riceTheorem_independent : RiceTheoremTarget := by
  intro C ⟨f, hf, hfC⟩ ⟨g, hg, hgC⟩ hdec
  exact hgC (ComputablePred.rice C hdec hf hg hfC)

#print axioms riceTheorem_independent
#print axioms ComputablePred.rice

end Stage1Instances.THM_M_0708.Validation
