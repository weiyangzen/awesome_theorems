import Statement

/-!
# THM-M-0767 proof-phase bodies

The exact frozen set-subtype target is closed by normalizing the cardinality
of the powerset and applying the pinned mathlib proof of Cantor's theorem.
-/

universe u

namespace Stage1.THM_M_0767

/-- The checked normalization used by the exact root composition. -/
theorem powerset_cardinality (alpha : Type u) (s : Set alpha) :
    Cardinal.mk (Set.powerset s) = 2 ^ Cardinal.mk s := by
  exact Cardinal.mk_powerset s

/-- Cantor's strict cardinal inequality at the subtype representing a set. -/
theorem cantor_for_set (alpha : Type u) (s : Set alpha) :
    Cardinal.mk s < 2 ^ Cardinal.mk s := by
  exact Cardinal.cantor (Cardinal.mk s)

/-- Exact proof of the canonical proposition frozen in `Statement.lean`. -/
theorem cantor_theorem : CanonicalTarget.{u} := by
  intro alpha s
  rw [powerset_cardinality alpha s]
  exact cantor_for_set alpha s

#print axioms powerset_cardinality
#print axioms cantor_for_set
#print axioms cantor_theorem

end Stage1.THM_M_0767
