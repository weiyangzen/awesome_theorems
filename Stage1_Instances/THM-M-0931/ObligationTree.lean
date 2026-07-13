import Statement
import Mathlib.Combinatorics.Additive.ErdosGinzburgZiv

/-!
# THM-M-0931 conditional obligation composition

This module checks the target-owned child-to-parent interfaces in the frozen
obligation graph. The indexed and multiset Erdos-Ginzburg-Ziv theorems remain
explicit premises or inspected candidates. Importing a candidate as the
canonical proof belongs to the proof phase, not this obligation-tree phase.
-/

namespace Stage1Instances.THM_M_0931.ObligationTree

open Finset

/-- The stronger at-least-cardinality integer multiset interface exposed by
the pinned mathlib candidate. -/
def AtLeastCountAnchor : Prop :=
  forall (n : Nat) (s : Multiset Int),
    2 * n - 1 <= s.card ->
      exists t : Multiset Int, t <= s /\ t.card = n /\ (n : Int) ∣ t.sum

/-- The indexed integer EGZ interface below the multiset wrapper. -/
def IndexedIntegerEGZ : Prop :=
  forall (ι : Type) (n : Nat) (s : Finset ι) (a : ι -> Int),
    2 * n - 1 <= s.card ->
      exists t : Finset ι, t ⊆ s /\ t.card = n /\
        (n : Int) ∣ ∑ i ∈ t, a i

/-- The occurrence-preserving enumeration crossing from an indexed EGZ
package to the multiset at-least-count package. -/
def MultisetEnumerationTransport : Prop :=
  IndexedIntegerEGZ -> AtLeastCountAnchor

/-- Specialization of the stronger at-least-count package to the positive,
exact-count canonical statement. -/
def ExactCountTransport : Prop :=
  AtLeastCountAnchor ->
    Stage1Instances.THM_M_0931.ErdosGinzburgZivTarget

/-- The exact terminal composition shape used at the root. -/
def RootComposition : Prop :=
  AtLeastCountAnchor -> ExactCountTransport ->
    Stage1Instances.THM_M_0931.ErdosGinzburgZivTarget

/-- Checked occurrence transport. The central indexed theorem is an explicit
premise; only enumeration and mapping back to a submultiset are proved here. -/
theorem multisetEnumerationTransport_checked :
    MultisetEnumerationTransport := by
  intro indexed n s hs
  obtain ⟨t, hts, ht⟩ :=
    indexed (Int × Nat) n s.toEnumFinset Prod.fst (by simpa using hs)
  exact ⟨t.1.map Prod.fst,
    Multiset.map_fst_le_of_subset_toEnumFinset hts, by simpa using ht⟩

/-- Checked child-to-parent composition for the multiset package. Both the
indexed engine and the enumeration transport are consumed. -/
theorem atLeastCountAnchor_of_indexed_and_enumeration
    (indexed : IndexedIntegerEGZ)
    (enumeration : MultisetEnumerationTransport) :
    AtLeastCountAnchor :=
  enumeration indexed

/-- Checked exact-count specialization, delegated to the statement phase's
already elaborated equality-to-lower-bound transport. -/
theorem exactCountTransport_checked : ExactCountTransport := by
  exact Stage1Instances.THM_M_0931.atLeastCountTarget_implies_erdosGinzburgZivTarget

/-- Checked terminal package. It does not supply the at-least-count anchor. -/
theorem rootComposition_checked : RootComposition := by
  intro anchor transport
  exact transport anchor

/-- Exact child-to-root composition. Every required child is explicit and
consumed; the pinned EGZ proof remains an uninstalled premise. -/
theorem root_of_terminal_packages
    (composition : RootComposition)
    (anchor : AtLeastCountAnchor)
    (transport : ExactCountTransport) :
    Stage1Instances.THM_M_0931.ErdosGinzburgZivTarget :=
  composition anchor transport

#check Int.erdos_ginzburg_ziv_multiset
#check Int.erdos_ginzburg_ziv
#check ZMod.erdos_ginzburg_ziv_multiset
#check ZMod.erdos_ginzburg_ziv
#check char_dvd_card_solutions_of_add_lt
#check multisetEnumerationTransport_checked
#check atLeastCountAnchor_of_indexed_and_enumeration
#check exactCountTransport_checked
#check rootComposition_checked
#check root_of_terminal_packages

#print axioms Int.erdos_ginzburg_ziv_multiset
#print axioms Int.erdos_ginzburg_ziv
#print axioms char_dvd_card_solutions_of_add_lt
#print axioms multisetEnumerationTransport_checked
#print axioms atLeastCountAnchor_of_indexed_and_enumeration
#print axioms exactCountTransport_checked
#print axioms rootComposition_checked
#print axioms root_of_terminal_packages

set_option pp.universes true in
set_option pp.explicit true in
#print Stage1Instances.THM_M_0931.ErdosGinzburgZivTarget

end Stage1Instances.THM_M_0931.ObligationTree
