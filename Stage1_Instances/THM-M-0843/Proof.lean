import ObligationTree
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0843 proof execution

This module adopts the exact regularity-lemma body from the manifest-pinned
mathlib dependency. It checks the frozen terminal-to-root composition and a
separate direct wrapper at the exact canonical target. Both wrappers share the
single upstream `szemeredi_regularity` body.
-/

namespace Stage1Instances.THM_M_0843.Proof

universe u

/-- The exact terminal interface, supplied by the pinned mathlib proof body. -/
theorem pinnedTerminal :
    Stage1Instances.THM_M_0843_Obligations.MathlibTerminal.{u} :=
  Stage1Instances.THM_M_0843_Obligations.pinned_mathlib_terminal

/-- Exact root closure through the child-to-parent composition frozen by the
obligation-tree phase. -/
theorem szemerediRegularity_via_frozen_composition :
    Stage1Instances.THM_M_0843.SzemerediRegularityTarget.{u} :=
  Stage1Instances.THM_M_0843_Obligations.compose_root
    Stage1Instances.THM_M_0843_Obligations.terminal_adapter pinnedTerminal

/-- A direct exact-type wrapper over the same pinned terminal body. -/
theorem szemerediRegularity :
    Stage1Instances.THM_M_0843.SzemerediRegularityTarget.{u} := by
  intro alpha _ _ G _ epsilon l hEpsilon hCard
  exact _root_.szemeredi_regularity G hEpsilon hCard

assert_no_sorry _root_.szemeredi_regularity
assert_no_sorry pinnedTerminal
assert_no_sorry szemerediRegularity_via_frozen_composition
assert_no_sorry szemerediRegularity

#print sorries _root_.szemeredi_regularity
#print sorries pinnedTerminal
#print sorries szemerediRegularity_via_frozen_composition
#print sorries szemerediRegularity

#print axioms _root_.szemeredi_regularity
#print axioms pinnedTerminal
#print axioms szemerediRegularity_via_frozen_composition
#print axioms szemerediRegularity

end Stage1Instances.THM_M_0843.Proof
