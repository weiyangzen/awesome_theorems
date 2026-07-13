import Mathlib.Combinatorics.Additive.ErdosGinzburgZiv

/-!
# THM-M-0931 anchor-audit probes

This module checks the frozen positive exact-count integer target through the
pinned mathlib Erdős-Ginzburg-Ziv theorem. The wrapper is candidate evidence
for the anchor-audit node only, not an accepted proof-phase declaration.
-/

namespace Stage1Instances.THM_M_0931_AnchorAudit

/-- Literal copy of the statement phase's frozen canonical proposition. -/
def ExactTarget : Prop :=
  forall (n : Nat), 0 < n -> forall (s : Multiset Int),
    s.card = 2 * n - 1 ->
      exists t : Multiset Int, t <= s /\ t.card = n /\ (n : Int) ∣ t.sum

/-- Exact adapter from the stronger pinned at-least-count theorem. -/
theorem exactTarget_mathlib_candidate : ExactTarget := by
  intro n _ s hs
  exact Int.erdos_ginzburg_ziv_multiset s hs.ge

#check Int.erdos_ginzburg_ziv_multiset
#check Int.erdos_ginzburg_ziv
#check ZMod.erdos_ginzburg_ziv_multiset
#check ZMod.erdos_ginzburg_ziv
#check char_dvd_card_solutions_of_add_lt

set_option pp.proofs false in
#print Int.erdos_ginzburg_ziv_multiset
set_option pp.proofs false in
#print Int.erdos_ginzburg_ziv
#print axioms Int.erdos_ginzburg_ziv_multiset
#print axioms Int.erdos_ginzburg_ziv
#print axioms ZMod.erdos_ginzburg_ziv_multiset
#print axioms ZMod.erdos_ginzburg_ziv
#print axioms char_dvd_card_solutions_of_add_lt
#print axioms exactTarget_mathlib_candidate

#print sorries Int.erdos_ginzburg_ziv_multiset
#print sorries exactTarget_mathlib_candidate

set_option pp.explicit true in
set_option pp.universes true in
#print ExactTarget

end Stage1Instances.THM_M_0931_AnchorAudit
