import ObligationTree

/-!
# THM-M-0708 proof execution

This module adopts the pinned mathlib Rice theorem audited by the preceding
phase, proves the frozen bridge interface, and composes it into the exact root.
-/

namespace Stage1Instances.THM_M_0708.Proof

open Nat.Partrec (Code)
open Nat.Partrec.Code
open Stage1Instances.THM_M_0708

/-- The frozen semantic-transfer bridge, discharged by the pinned mathlib
implementation of Rice's theorem. -/
theorem riceBridge : RiceBridge := by
  intro C f g hdec hf hg hfC
  exact ComputablePred.rice C hdec hf hg hfC

/-- The exact frozen functional Rice theorem. -/
theorem riceTheorem : RiceTheoremTarget :=
  root_of_riceBridge riceBridge

/-- A direct proof of the exact root, retained as an exact-type cross-check of
the frozen composition route. -/
theorem riceTheorem_direct : RiceTheoremTarget := by
  intro C ⟨f, hf, hfC⟩ ⟨g, hg, hgC⟩ hdec
  exact hgC (ComputablePred.rice C hdec hf hg hfC)

#print axioms riceBridge
#print axioms riceTheorem
#print axioms riceTheorem_direct

end Stage1Instances.THM_M_0708.Proof
