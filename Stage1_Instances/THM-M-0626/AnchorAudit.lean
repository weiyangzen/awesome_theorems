import Mathlib.Topology.Connected.Basic

/-!
# THM-M-0626 anchor-audit probes

This module compares a literal copy of the frozen global-continuity target with the sharper pinned
mathlib theorem. The wrapper is candidate evidence for the anchor-audit node, not an accepted
proof-phase declaration or theorem-completion receipt.
-/

namespace Stage1Instances.THM_M_0626_AnchorAudit

universe u v

/-- Literal audit copy of the statement gate's canonical proposition. -/
def ExactTarget : Prop :=
  ∀ {α : Type u} {β : Type v} [TopologicalSpace α] [TopologicalSpace β]
    {s : Set α}, IsConnected s → ∀ f : α → β, Continuous f → IsConnected (f '' s)

/-- Exact adapter from global continuity to mathlib's stronger `ContinuousOn` candidate. -/
theorem exactTarget_mathlib_candidate : ExactTarget.{u, v} := by
  intro α β _ _ s hs f hf
  exact hs.image f hf.continuousOn

#check IsPreconnected.image
#check IsConnected.image
#check Continuous.continuousOn
#check isConnected_range
#check Function.Surjective.connectedSpace

#print IsPreconnected.image
#print IsConnected.image
#print axioms IsPreconnected.image
#print axioms IsConnected.image
#print axioms exactTarget_mathlib_candidate
#print sorries IsPreconnected.image
#print sorries IsConnected.image
#print sorries exactTarget_mathlib_candidate

set_option pp.universes true in
set_option pp.explicit true in
#print ExactTarget

end Stage1Instances.THM_M_0626_AnchorAudit
