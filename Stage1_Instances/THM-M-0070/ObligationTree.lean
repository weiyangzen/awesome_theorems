import Statement

/-!
# THM-M-0070 conditional obligation composition

This module checks the local child-to-root interfaces frozen by the obligation registry. The
placeholder-free Lean translation remains an explicit premise. The Coq/MathComp source cannot be
imported into Lean, so nothing in this module proves the odd-order theorem.
-/

noncomputable section

namespace Stage1Instances.THM_M_0070.ObligationTree

universe u

/-- Type required from a future placeholder-free Lean translation of the external architecture. -/
def TranslatedOddOrderBody : Prop :=
  Stage1Instances.THM_M_0070.OddOrderSolvabilityTarget.{u}

/-- The translated-body boundary is definitionally the exact frozen target, not a weaker claim. -/
theorem translatedOddOrderBody_iff_target :
    TranslatedOddOrderBody.{u} <->
      Stage1Instances.THM_M_0070.OddOrderSolvabilityTarget.{u} :=
  Iff.rfl

/-- Conditional adapter: consume the full translated conclusion without adding a premise. -/
theorem target_of_translatedOddOrderBody
    (body : TranslatedOddOrderBody.{u}) :
    Stage1Instances.THM_M_0070.OddOrderSolvabilityTarget.{u} :=
  body

/-- Terminal composition consumes the exact adapter output. -/
theorem terminalTarget_of_target
    (target : Stage1Instances.THM_M_0070.OddOrderSolvabilityTarget.{u}) :
    Stage1Instances.THM_M_0070.OddOrderSolvabilityTarget.{u} :=
  target

/-- Root composition consumes the exact terminal conclusion. -/
theorem root_of_terminalTarget
    (terminal : Stage1Instances.THM_M_0070.OddOrderSolvabilityTarget.{u}) :
    Stage1Instances.THM_M_0070.OddOrderSolvabilityTarget.{u} :=
  terminal

#print axioms translatedOddOrderBody_iff_target
#print axioms target_of_translatedOddOrderBody
#print axioms terminalTarget_of_target
#print axioms root_of_terminalTarget

set_option pp.universes true in
set_option pp.explicit true in
#print TranslatedOddOrderBody

end Stage1Instances.THM_M_0070.ObligationTree
