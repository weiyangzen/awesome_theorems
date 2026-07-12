import Mathlib.ModelTheory.ElementarySubstructures

/-!
# THM-M-0650: immutable anchor audit

This module checks the exact pinned mathlib proof anchor and its immediate
embedding proof body. It is audit evidence, not the theorem-phase wrapper.
-/

namespace Stage1Instances.THM_M_0650.AnchorAudit

universe u v w

open FirstOrder

/-- The frozen target, restated so this audit remains a narrowly scoped Lean
check rather than depending on an unregistered local module import. -/
def AuditedTarget : Prop :=
  forall (L : FirstOrder.Language.{v, w}) (M : Type u) [L.Structure M]
      (S : L.Substructure M),
    (forall (n : Nat) (phi : L.BoundedFormula Empty (n + 1))
        (x : Fin n -> S) (a : M),
      phi.Realize default (Fin.snoc ((↑) ∘ x) a : _ -> M) ->
        exists b : S,
          phi.Realize default (Fin.snoc ((↑) ∘ x) b : _ -> M)) ->
      S.IsElementary

/-- Exact repo-local closure through the audited pinned declaration. -/
theorem auditedTarget_of_pinnedMathlib : AuditedTarget.{u, v, w} := by
  intro L M _ S h
  exact S.isElementary_of_exists h

#check FirstOrder.Language.Substructure.isElementary_of_exists
#check FirstOrder.Language.Embedding.isElementary_of_exists
#check FirstOrder.Language.Substructure.toElementarySubstructure
#print axioms auditedTarget_of_pinnedMathlib
#print axioms FirstOrder.Language.Substructure.isElementary_of_exists
#print axioms FirstOrder.Language.Embedding.isElementary_of_exists

end Stage1Instances.THM_M_0650.AnchorAudit
