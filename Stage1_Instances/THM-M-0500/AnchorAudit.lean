import Mathlib.NumberTheory.LSeries.PrimesInAP

/-!
# THM-M-0500 pinned mathlib anchor audit

This module checks the exact canonical proposition against the proof-bearing declaration in the
pinned mathlib checkout. It is audit evidence only; the later proof phase owns any public wrapper.
-/

namespace Stage1Instances.THM_M_0500.AnchorAudit

def AuditedTarget : Prop :=
  ∀ (q : ℕ) [NeZero q] (a : ZMod q), IsUnit a →
    {p : ℕ | p.Prime ∧ (p : ZMod q) = a}.Infinite

/-- Exact-type candidate check. No transport or weakened statement is used. -/
theorem pinnedMathlibCandidate : AuditedTarget := by
  intro q _ a ha
  exact Nat.infinite_setOf_prime_and_eq_mod ha

#check Nat.infinite_setOf_prime_and_eq_mod
#check Nat.forall_exists_prime_gt_and_eq_mod
#check Nat.infinite_setOf_prime_and_modEq
#print Nat.infinite_setOf_prime_and_eq_mod
#print axioms Nat.infinite_setOf_prime_and_eq_mod
#print axioms pinnedMathlibCandidate

end Stage1Instances.THM_M_0500.AnchorAudit
