import Statement

/-!
# THM-M-0958 conditional obligation composition

This module checks only the exact terminal interfaces selected by the frozen
Elkin obligation architecture. The construction-witness theorem is an
explicit hypothesis, so no instance of Elkin's lower bound is proved here.
-/

noncomputable section

namespace Stage1Instances.THM_M_0958.ObligationTree

open Stage1Instances.THM_M_0958

/-- Exact witness-form output of the annulus, discrepancy, embedding, and
parameter-optimization route. -/
def ConstructionWitnessPackage : Prop := WitnessConstructionTarget

/-- Exact checked direction from the source witness form to the canonical
one-based extremal form. -/
def WitnessToRootTransport : Prop :=
  ConstructionWitnessPackage -> ElkinConstructionTarget

/-- Exact terminal child-to-root composition shape. -/
def RootComposition : Prop :=
  ConstructionWitnessPackage -> WitnessToRootTransport ->
    ElkinConstructionTarget

/-- The statement phase already checked this direction of the witness/extremal
equivalence. It supplies no construction witness. -/
theorem checkedWitnessToRootTransport : WitnessToRootTransport := by
  exact elkinConstructionTarget_iff_witnessConstructionTarget.mpr

/-- Checked composition shape. Both the witness and its exact transport are
consumed, while neither is manufactured. -/
theorem rootComposition_checked : RootComposition := by
  intro witness transport
  exact transport witness

/-- Exact conditional root harness binding all declared terminal children. -/
theorem root_of_terminal_packages
    (composition : RootComposition)
    (witness : ConstructionWitnessPackage)
    (transport : WitnessToRootTransport) : ElkinConstructionTarget :=
  composition witness transport

#check ConstructionWitnessPackage
#check WitnessToRootTransport
#check RootComposition
#check checkedWitnessToRootTransport
#check rootComposition_checked
#check root_of_terminal_packages

#print axioms checkedWitnessToRootTransport
#print axioms rootComposition_checked
#print axioms root_of_terminal_packages

end Stage1Instances.THM_M_0958.ObligationTree
