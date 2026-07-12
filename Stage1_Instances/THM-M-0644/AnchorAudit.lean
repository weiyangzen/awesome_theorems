import Mathlib.ModelTheory.Satisfiability

/-!
Pinned anchor certificate for the first-order compactness target. The wrapper deliberately repeats
the frozen target type so that elaboration checks the upstream declaration without importing any
later proof artifact from this dossier.
-/

namespace Stage1.THM_M_0644.AnchorAudit

open FirstOrder

universe u v

theorem exactMathlibAnchor {L : Language.{u, v}} {T : L.Theory} :
    T.IsSatisfiable ↔ T.IsFinitelySatisfiable :=
  FirstOrder.Language.Theory.isSatisfiable_iff_isFinitelySatisfiable

#check FirstOrder.Language.Theory.IsSatisfiable.isFinitelySatisfiable
#check FirstOrder.Language.Theory.isSatisfiable_iff_isFinitelySatisfiable
#check exactMathlibAnchor
#print axioms FirstOrder.Language.Theory.isSatisfiable_iff_isFinitelySatisfiable
#print axioms exactMathlibAnchor

end Stage1.THM_M_0644.AnchorAudit
