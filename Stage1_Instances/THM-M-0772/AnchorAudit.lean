import Mathlib.Order.CompleteLattice.Chain

/-!
# THM-M-0772: pinned mathlib anchor audit

This module checks the discovered mathlib candidate at the exact target type.
It is an audit fixture, not the canonical theorem implementation.
-/

namespace Stage1Instances.THM_M_0772.AnchorAudit

universe u

/-- The statement frozen by `Statement.lean`, repeated here so this audit has one proof-bearing
direct import and cannot acquire the statement phase's declaration through a broad umbrella import. -/
def AuditedTarget : Prop :=
  ∀ (P : Type u) [PartialOrder P], ∃ c : Set P, IsMaxChain (· ≤ ·) c

/-- Exact adapter from mathlib's relation-generic Hausdorff maximality theorem. -/
theorem mathlib_maxChain_spec_candidate : AuditedTarget.{u} := by
  intro P _order
  exact ⟨maxChain (· ≤ ·), maxChain_spec⟩

end Stage1Instances.THM_M_0772.AnchorAudit

#check @maxChain_spec
#print axioms maxChain_spec
#print axioms Stage1Instances.THM_M_0772.AnchorAudit.mathlib_maxChain_spec_candidate
