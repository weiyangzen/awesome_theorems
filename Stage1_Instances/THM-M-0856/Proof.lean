import ObligationTree
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

set_option autoImplicit false

/-!
# THM-M-0856 proof-phase installation

This module installs the exact Tutte theorem from the manifest-pinned mathlib dependency at the
terminal interface frozen by `ObligationTree.lean`. It then consumes the frozen adapter and terminal
children to obtain the canonical target. A direct exact-target wrapper independently checks the
same single upstream proof body.
-/

namespace Stage1Instances.THM_M_0856.Proof

universe u

open SimpleGraph
open Stage1Instances.THM_M_0856
open Stage1Instances.THM_M_0856.ObligationTree

/-- The manifest-pinned mathlib theorem installed at the frozen terminal interface. -/
theorem pinnedTerminal : MathlibTerminal.{u} :=
  pinned_mathlib_terminal

/-- Exact canonical root obtained through the frozen two-child composition. -/
theorem tutteOneFactor_via_frozen_composition : TutteOneFactorTarget.{u} :=
  compose_root terminal_adapter pinnedTerminal

/-- A direct exact-target wrapper over the same pinned terminal proof body. -/
theorem tutteOneFactor_direct : TutteOneFactorTarget.{u} := by
  intro V G _
  simpa only [OddComponentCondition, SimpleGraph.IsTutteViolator, not_lt] using
    (SimpleGraph.tutte (G := G))

#check pinnedTerminal
#check tutteOneFactor_via_frozen_composition
#check tutteOneFactor_direct

assert_no_sorry SimpleGraph.tutte
assert_no_sorry pinnedTerminal
assert_no_sorry tutteOneFactor_via_frozen_composition
assert_no_sorry tutteOneFactor_direct

#print sorries SimpleGraph.tutte
#print sorries pinnedTerminal
#print sorries tutteOneFactor_via_frozen_composition
#print sorries tutteOneFactor_direct

#print axioms SimpleGraph.tutte
#print axioms pinnedTerminal
#print axioms tutteOneFactor_via_frozen_composition
#print axioms tutteOneFactor_direct

end Stage1Instances.THM_M_0856.Proof
