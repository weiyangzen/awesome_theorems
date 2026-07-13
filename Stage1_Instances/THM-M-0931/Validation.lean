import Statement
import Mathlib.Combinatorics.Additive.ErdosGinzburgZiv
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0931 differential validation reconstruction

This module imports the frozen statement and the pinned mathlib theorem directly.
It deliberately does not import the proof-phase module or obligation-tree module.
The exact root is reconstructed through indexed occurrences rather than the public
multiset wrapper used by the direct proof-phase route.
-/

namespace Stage1Instances.THM_M_0931.Validation

open Stage1Instances.THM_M_0931

/-- A separately written reconstruction of the exact frozen target through the
indexed integer theorem and the input multiset's occurrence enumeration. This is
same-worker differential evidence, not an independent-runner attestation. -/
theorem independentlyReconstructedErdosGinzburgZiv :
    ErdosGinzburgZivTarget := by
  intro n _ s hs
  obtain ⟨t, hts, ht⟩ :=
    Int.erdos_ginzburg_ziv Prod.fst (s := s.toEnumFinset) (by simpa using hs.ge)
  exact ⟨t.1.map Prod.fst,
    Multiset.map_fst_le_of_subset_toEnumFinset hts, by simpa using ht⟩

#check independentlyReconstructedErdosGinzburgZiv
assert_no_sorry Int.erdos_ginzburg_ziv
assert_no_sorry char_dvd_card_solutions_of_add_lt
assert_no_sorry independentlyReconstructedErdosGinzburgZiv
#print sorries Int.erdos_ginzburg_ziv
#print sorries char_dvd_card_solutions_of_add_lt
#print sorries independentlyReconstructedErdosGinzburgZiv
#print axioms Int.erdos_ginzburg_ziv
#print axioms char_dvd_card_solutions_of_add_lt
#print axioms independentlyReconstructedErdosGinzburgZiv

end Stage1Instances.THM_M_0931.Validation
