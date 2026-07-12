import Mathlib.Topology.Homotopy.HomotopyGroup

/-!
# THM-M-0557: pinned formal-anchor audit

This file checks the exact pinned mathlib route for the frozen statement. It is
candidate evidence for the anchor-audit node, not downstream proof acceptance.
-/

namespace Stage1Instances.THM_M_0557.AnchorAudit

universe u

/-- Direct exact-type probe for the group and commutative-group instances in
the pinned `HomotopyGroup` module. -/
theorem pinnedMathlibCandidate :
    forall (X : Type u) [TopologicalSpace X] (x : X) (n : Nat),
      Nonempty (Group (HomotopyGroup.Pi (n + 1) X x)) /\
        Nonempty (CommGroup (HomotopyGroup.Pi (n + 2) X x)) := by
  intro X _ x n
  exact ⟨⟨inferInstance⟩, ⟨inferInstance⟩⟩

#check HomotopyGroup.group
#check HomotopyGroup.commGroup
#check GenLoop.loopHomeo
#check homotopyGroupEquivFundamentalGroup
#check HomotopyGroup.auxGroup_indep
#check HomotopyGroup.isUnital_auxGroup
#print axioms pinnedMathlibCandidate

end Stage1Instances.THM_M_0557.AnchorAudit
