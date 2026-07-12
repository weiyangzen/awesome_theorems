import Mathlib.ModelTheory.Satisfiability

/-!
# THM-M-0698: pinned formal anchor audit

This module checks the exact compactness candidate in the manifest-pinned
mathlib dependency. Proof-state promotion belongs to later workflow phases.
-/

namespace Stage1Instances.THM_M_0698.AnchorAudit

open FirstOrder

universe u v

/-- The frozen target, repeated here so this audit has a narrow standalone check. -/
def AuditedTarget : Prop :=
  forall {L : FirstOrder.Language.{u, v}} {T : L.Theory},
    T.IsSatisfiable <-> T.IsFinitelySatisfiable

/-- Exact wrapper around the terminal theorem in pinned mathlib. -/
theorem pinnedMathlibCandidateClosesAuditedTarget : AuditedTarget.{u, v} := by
  intro L T
  exact FirstOrder.Language.Theory.isSatisfiable_iff_isFinitelySatisfiable

#check FirstOrder.Language.Theory.IsSatisfiable
#check FirstOrder.Language.Theory.IsFinitelySatisfiable
#check FirstOrder.Language.Theory.IsSatisfiable.isFinitelySatisfiable
#check FirstOrder.Language.Theory.isSatisfiable_iff_isFinitelySatisfiable
#print axioms FirstOrder.Language.Theory.isSatisfiable_iff_isFinitelySatisfiable
#print axioms pinnedMathlibCandidateClosesAuditedTarget

end Stage1Instances.THM_M_0698.AnchorAudit
