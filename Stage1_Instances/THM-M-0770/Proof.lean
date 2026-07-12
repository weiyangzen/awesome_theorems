import Statement

/-!
# THM-M-0770 proof execution

This module closes the exact frozen Zorn target with the audited theorem from
the repository's pinned mathlib dependency.
-/

namespace Stage1Instances.THM_M_0770.Proof

open Stage1Instances.THM_M_0770

universe u

/-- Every nonempty partial order in which each nonempty chain has an upper
bound contains a maximal element. -/
theorem zornsLemma : ZornsLemmaTarget.{u} := by
  intro alpha _ _ chains_bounded
  exact zorn_le_nonempty chains_bounded

#print axioms zornsLemma

end Stage1Instances.THM_M_0770.Proof
