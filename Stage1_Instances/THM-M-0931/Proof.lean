import ObligationTree
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0931 proof execution

This module adopts the integer Erdős-Ginzburg-Ziv bodies from the manifest-pinned
mathlib dependency. It checks the exact frozen root through the indexed occurrence
route and independently through the public multiset theorem. Both routes share the
same upstream indexed proof body and therefore receive no duplicate proof credit.
-/

namespace Stage1Instances.THM_M_0931.Proof

open Stage1Instances.THM_M_0931
open Stage1Instances.THM_M_0931.ObligationTree

/-- The indexed integer engine installed at its frozen interface. -/
theorem pinnedIndexedIntegerEGZ : IndexedIntegerEGZ := by
  intro ι n s a hs
  exact Int.erdos_ginzburg_ziv a hs

/-- The public pinned multiset theorem installed at the exact at-least-count interface. -/
theorem pinnedAtLeastCountAnchor : AtLeastCountAnchor := by
  intro n s hs
  exact Int.erdos_ginzburg_ziv_multiset s hs

/-- The at-least-count anchor reconstructed through the frozen occurrence transport. -/
theorem atLeastCountAnchor_via_frozen_enumeration : AtLeastCountAnchor :=
  atLeastCountAnchor_of_indexed_and_enumeration pinnedIndexedIntegerEGZ
    multisetEnumerationTransport_checked

/-- Exact root closure through every checked child in the frozen proof graph. -/
theorem erdosGinzburgZiv_via_frozen_composition : ErdosGinzburgZivTarget :=
  root_of_terminal_packages rootComposition_checked
    atLeastCountAnchor_via_frozen_enumeration exactCountTransport_checked

/-- A direct exact-type wrapper over the same pinned terminal route. -/
theorem erdosGinzburgZiv_direct : ErdosGinzburgZivTarget := by
  intro n _ s hs
  exact Int.erdos_ginzburg_ziv_multiset s hs.ge

/-- The target-owned canonical proof declaration. -/
theorem erdosGinzburgZiv : ErdosGinzburgZivTarget :=
  erdosGinzburgZiv_via_frozen_composition

assert_no_sorry Int.erdos_ginzburg_ziv_multiset
assert_no_sorry Int.erdos_ginzburg_ziv
assert_no_sorry char_dvd_card_solutions_of_add_lt
assert_no_sorry pinnedIndexedIntegerEGZ
assert_no_sorry pinnedAtLeastCountAnchor
assert_no_sorry atLeastCountAnchor_via_frozen_enumeration
assert_no_sorry erdosGinzburgZiv_via_frozen_composition
assert_no_sorry erdosGinzburgZiv_direct
assert_no_sorry erdosGinzburgZiv

#print sorries Int.erdos_ginzburg_ziv_multiset
#print sorries Int.erdos_ginzburg_ziv
#print sorries char_dvd_card_solutions_of_add_lt
#print sorries pinnedIndexedIntegerEGZ
#print sorries pinnedAtLeastCountAnchor
#print sorries atLeastCountAnchor_via_frozen_enumeration
#print sorries erdosGinzburgZiv_via_frozen_composition
#print sorries erdosGinzburgZiv_direct
#print sorries erdosGinzburgZiv

#print axioms Int.erdos_ginzburg_ziv_multiset
#print axioms Int.erdos_ginzburg_ziv
#print axioms char_dvd_card_solutions_of_add_lt
#print axioms pinnedIndexedIntegerEGZ
#print axioms pinnedAtLeastCountAnchor
#print axioms atLeastCountAnchor_via_frozen_enumeration
#print axioms erdosGinzburgZiv_via_frozen_composition
#print axioms erdosGinzburgZiv_direct
#print axioms erdosGinzburgZiv

end Stage1Instances.THM_M_0931.Proof
