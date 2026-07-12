import Mathlib.Order.Zorn

/-!
# THM-M-0770 obligation-tree composition probes

These declarations check only the typed interfaces frozen by the obligation
registry. The imported Zorn theorem is deliberately represented by an
abstract child hypothesis here; this phase does not claim proof-node credit.
-/

namespace Stage1Instances.THM_M_0770.ObligationTree

universe u

/-- Local exact copy of the fingerprinted canonical statement. The validator
binds this module to `Statement.lean` and the frozen expression hash. -/
def CanonicalTarget : Prop :=
  ∀ (alpha : Type u) [PartialOrder alpha] [Nonempty alpha],
    (∀ c : Set alpha, IsChain (fun x y => x <= y) c -> c.Nonempty -> BddAbove c) ->
      ∃ m : alpha, IsMax m

/-- Exact signature of the audited upstream bridge after specializing its
`Preorder` parameter to the canonical `PartialOrder`. -/
def AuditedAnchorTarget : Prop :=
  ∀ (alpha : Type u) [PartialOrder alpha] [Nonempty alpha],
    (∀ c : Set alpha, IsChain (fun x y => x <= y) c -> c.Nonempty -> BddAbove c) ->
      ∃ m : alpha, IsMax m

/-- Checked statement transport from the audited bridge interface to the root. -/
theorem root_of_audited_anchor (h : AuditedAnchorTarget.{u}) :
    CanonicalTarget.{u} :=
  h

/-- Reverse identity transport prevents the graph from hiding a strengthened
or weakened anchor interface. -/
theorem audited_anchor_of_root
    (h : CanonicalTarget.{u}) :
    AuditedAnchorTarget.{u} :=
  h

end Stage1Instances.THM_M_0770.ObligationTree

#print axioms Stage1Instances.THM_M_0770.ObligationTree.root_of_audited_anchor
#print axioms Stage1Instances.THM_M_0770.ObligationTree.audited_anchor_of_root
