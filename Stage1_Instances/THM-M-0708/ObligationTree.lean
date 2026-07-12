import Mathlib.Computability.Halting

/-!
# THM-M-0708 conditional obligation composition

This file checks the composition chosen by the frozen architecture. The
central Rice bridge is deliberately an explicit premise: adopting the audited
mathlib body belongs to the proof phase, not this obligation-tree phase.
-/

namespace Stage1Instances.THM_M_0708

open Nat.Partrec (Code)
open Nat.Partrec.Code

/-- Exact re-elaboration of the separately frozen statement, kept here so the
node-scoped check does not require mutating Lake's build cache. -/
def RiceTheoremTarget : Prop :=
  forall C : Set (Nat →. Nat),
    (exists f : Nat →. Nat, Nat.Partrec f /\ f ∈ C) ->
    (exists g : Nat →. Nat, Nat.Partrec g /\ g ∉ C) ->
    Not (ComputablePred fun c : Code => eval c ∈ C)

/-- Exact interface expected from the central imported Rice theorem. -/
def RiceBridge : Prop :=
  forall (C : Set (Nat →. Nat)) (f g : Nat →. Nat),
    ComputablePred (fun c : Code => eval c ∈ C) ->
    Nat.Partrec f -> Nat.Partrec g -> f ∈ C -> g ∈ C

/-- Checked child-to-root composition. This consumes the positive and negative
witnesses and the exact bridge conclusion; it does not prove `RiceBridge`. -/
theorem root_of_riceBridge (bridge : RiceBridge) : RiceTheoremTarget := by
  intro C ⟨f, hf, fC⟩ ⟨g, hg, gC⟩ hdec
  exact gC (bridge C f g hdec hf hg fC)

#print axioms root_of_riceBridge

end Stage1Instances.THM_M_0708
