import ObligationTree
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0484 proof execution

This module installs the two exact Lucas-Lehmer correctness directions from the
manifest-pinned mathlib dependency. It then consumes the frozen direction-to-root
and terminal-to-root composition certificates. All local declarations share the
two upstream terminal proof bodies.
-/

set_option autoImplicit false

namespace Stage1Instances.THM_M_0484.Proof

open Stage1Instances.THM_M_0484

/-- The forward terminal interface supplied by pinned mathlib. -/
theorem pinnedSufficiency : ObligationTree.SufficiencyTarget := by
  intro p hp htest
  exact lucas_lehmer_sufficiency p (by omega) htest

/-- The reverse terminal interface supplied by pinned mathlib. -/
theorem pinnedNecessity : ObligationTree.NecessityTarget := by
  intro p hp hprime
  exact lucas_lehmer_necessity p hp hprime

/-- The exact root assembled from both frozen direction interfaces. -/
theorem assembledRoot : LucasLehmerTestTarget :=
  ObligationTree.root_of_directions
    (ObligationTree.sufficiency_of_branch pinnedSufficiency)
    (ObligationTree.necessity_of_branch pinnedNecessity)

/-- The canonical target through the final frozen terminal composition. -/
theorem lucasLehmerCriterion : LucasLehmerTestTarget :=
  ObligationTree.root_of_terminal assembledRoot

assert_no_sorry lucas_lehmer_sufficiency
assert_no_sorry lucas_lehmer_necessity
assert_no_sorry pinnedSufficiency
assert_no_sorry pinnedNecessity
assert_no_sorry assembledRoot
assert_no_sorry lucasLehmerCriterion

#print sorries lucas_lehmer_sufficiency lucas_lehmer_necessity
  pinnedSufficiency pinnedNecessity assembledRoot lucasLehmerCriterion

#print axioms lucas_lehmer_sufficiency
#print axioms lucas_lehmer_necessity
#print axioms pinnedSufficiency
#print axioms pinnedNecessity
#print axioms assembledRoot
#print axioms lucasLehmerCriterion

end Stage1Instances.THM_M_0484.Proof
