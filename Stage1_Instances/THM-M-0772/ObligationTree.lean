import Mathlib.Order.CompleteLattice.Chain

/-!
# THM-M-0772: obligation-tree composition fixture

This file checks the frozen child-to-parent interface.  The hypothesis of
`root_of_relationGenericMaxChain` deliberately represents the imported bridge
obligation; this phase does not install it as the canonical theorem proof.
-/

namespace Stage1Instances.THM_M_0772.ObligationTree

universe u

/-- The exact canonical target, repeated under the proof-architecture import. -/
def CanonicalTarget : Prop :=
  ∀ (P : Type u) [PartialOrder P], ∃ c : Set P, IsMaxChain (· ≤ ·) c

/-- The relation-generic bridge conclusion supplied by the audited mathlib body. -/
def RelationGenericMaxChain : Prop :=
  ∀ (P : Type u) (r : P → P → Prop), ∃ c : Set P, IsMaxChain r c

/-- Checked composition: specialize the relation-generic bridge and package its witness. -/
theorem root_of_relationGenericMaxChain
    (bridge : RelationGenericMaxChain.{u}) : CanonicalTarget.{u} := by
  intro P _order
  exact bridge P (· ≤ ·)

/-- The frozen bridge signature is exactly inhabited by the audited terminal declaration. -/
theorem audited_bridge_signature : RelationGenericMaxChain.{u} := by
  intro P r
  exact ⟨maxChain r, maxChain_spec⟩

end Stage1Instances.THM_M_0772.ObligationTree

#print axioms maxChain_spec
#print axioms Stage1Instances.THM_M_0772.ObligationTree.root_of_relationGenericMaxChain
#print axioms Stage1Instances.THM_M_0772.ObligationTree.audited_bridge_signature
