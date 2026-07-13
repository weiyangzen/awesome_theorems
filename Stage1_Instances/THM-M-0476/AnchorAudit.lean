import Mathlib.NumberTheory.Wilson

/-!
# THM-M-0476 anchor-audit probes

This module checks the exact frozen target through the pinned mathlib Wilson theorem and records
the nearby theorem family. The wrapper is candidate evidence for the anchor-audit node only; it is
not an accepted proof-phase declaration or a theorem-completion claim.
-/

open scoped Nat

namespace Stage1Instances.THM_M_0476_AnchorAudit

/-- Literal copy of the statement phase's frozen canonical proposition. -/
def ExactTarget : Prop :=
  forall (p : Nat), p.Prime -> ((p - 1)! : ZMod p) = -1

/-- Exact explicit-premise adapter to the pinned typeclass-premise mathlib theorem. -/
theorem exactTarget_mathlib_candidate : ExactTarget := by
  intro p hp
  letI : Fact p.Prime := ⟨hp⟩
  exact ZMod.wilsons_lemma p

#check ZMod.wilsons_lemma
#check ZMod.prod_Ico_one_prime
#check Nat.prime_of_fac_equiv_neg_one
#check Nat.prime_iff_fac_equiv_neg_one
#check FiniteField.prod_univ_units_id_eq_neg_one

set_option pp.proofs false in
#print ZMod.wilsons_lemma
set_option pp.proofs false in
#print Nat.prime_iff_fac_equiv_neg_one
#print axioms ZMod.wilsons_lemma
#print axioms ZMod.prod_Ico_one_prime
#print axioms Nat.prime_of_fac_equiv_neg_one
#print axioms Nat.prime_iff_fac_equiv_neg_one
#print axioms FiniteField.prod_univ_units_id_eq_neg_one
#print axioms exactTarget_mathlib_candidate

#print sorries ZMod.wilsons_lemma
#print sorries exactTarget_mathlib_candidate

set_option pp.explicit true in
set_option pp.universes true in
#print ExactTarget

end Stage1Instances.THM_M_0476_AnchorAudit
