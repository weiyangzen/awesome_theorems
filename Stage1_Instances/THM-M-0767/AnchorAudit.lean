import Mathlib.SetTheory.Cardinal.Order

universe u

namespace Stage1.THM_M_0767.AnchorAudit

/-- A checked wrapper showing that pinned mathlib's `Cardinal.cantor` closes the
canonical set-subtype statement after the audited `mk_powerset` normalization. -/
theorem mathlib_anchor :
    ∀ (alpha : Type u) (s : Set alpha),
      Cardinal.mk s < Cardinal.mk (Set.powerset s) := by
  intro alpha s
  rw [Cardinal.mk_powerset]
  exact Cardinal.cantor (Cardinal.mk s)

/-- The direct diagonal boundary used by the cardinal theorem's terminal body. -/
example (alpha : Type u) (f : alpha → Set alpha) : ¬Function.Surjective f :=
  Function.cantor_surjective f

end Stage1.THM_M_0767.AnchorAudit

#check Cardinal.cantor
#check Cardinal.mk_powerset
#check Function.cantor_injective
#check Function.cantor_surjective
#print axioms Cardinal.cantor
#print axioms Cardinal.mk_powerset
#print axioms Function.cantor_injective
#print axioms Function.cantor_surjective
#print axioms Stage1.THM_M_0767.AnchorAudit.mathlib_anchor
