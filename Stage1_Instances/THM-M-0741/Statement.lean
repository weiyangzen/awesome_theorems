import Mathlib.Computability.Halting

/-!
# THM-M-0741 canonical Lean statement

This module freezes the arbitrary-program/arbitrary-input halting predicate for mathlib's
universal partial-recursive-code model. It checks the statement boundary only and contains no
proof of undecidability.
-/

namespace Stage1Instances.THM_M_0741

open Nat.Partrec

/-- A partial-recursive code halts on an input exactly when its universal evaluation is defined. -/
def Halts (programInput : Code × Nat) : Prop :=
  (Code.eval programInput.1 programInput.2).Dom

/-- No one total effective Boolean procedure decides halting for every program and input. -/
def HaltingProblemUndecidable : Prop :=
  Not (ComputablePred Halts)

/-- The canonical target with the local halting predicate expanded. -/
def ExpandedHaltingProblemUndecidable : Prop :=
  Not (ComputablePred fun programInput : Code × Nat =>
    (Code.eval programInput.1 programInput.2).Dom)

/-- Checked identity between the named and expanded statement encodings. -/
theorem haltingProblemUndecidable_iff_expanded :
    HaltingProblemUndecidable <-> ExpandedHaltingProblemUndecidable :=
  Iff.rfl

/-! Structural mutations elaborate as propositions but receive no statement-identity credit. -/

def mutationRemovedEffectivity : Prop :=
  Not (exists d : Code × Nat -> Bool,
    forall programInput, d programInput = true <-> Halts programInput)

def mutationChangedDomainToPrograms : Prop :=
  forall input : Nat,
    Not (ComputablePred fun program : Code => (Code.eval program input).Dom)

def mutationChangedBinderScope : Prop :=
  exists input : Nat,
    Not (ComputablePred fun program : Code => (Code.eval program input).Dom)

def mutationChangedBoundaryToSelfInput : Prop :=
  Not (ComputablePred fun program : Code =>
    (Code.eval program program.encodeCode).Dom)

variable
  (hCanonical : HaltingProblemUndecidable)
  (hEffectivity : mutationRemovedEffectivity)
  (hDomain : mutationChangedDomainToPrograms)
  (hScope : mutationChangedBinderScope)
  (hBoundary : mutationChangedBoundaryToSelfInput)

#check_failure (show mutationRemovedEffectivity from hCanonical)
#check_failure (show HaltingProblemUndecidable from hEffectivity)
#check_failure (show HaltingProblemUndecidable from hDomain)
#check_failure (show HaltingProblemUndecidable from hScope)
#check_failure (show HaltingProblemUndecidable from hBoundary)

/-! Boundary witnesses authenticate the selected execution semantics only. -/

/-- The zero code returns zero, so it halts on every natural-number input, including zero. -/
theorem zero_halts (input : Nat) : Halts (Code.zero, input) := by
  exact Part.some_dom 0

/-- Searching for a zero of the successor function diverges on every input. -/
theorem rfind_succ_does_not_halt (input : Nat) :
    Not (Halts (Code.rfind' Code.succ, input)) := by
  simp [Halts, Code.eval]

#check haltingProblemUndecidable_iff_expanded
#print axioms haltingProblemUndecidable_iff_expanded

set_option pp.universes true in
set_option pp.explicit true in
#print HaltingProblemUndecidable

end Stage1Instances.THM_M_0741
