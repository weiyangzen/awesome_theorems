import ObligationTree

/-!
# THM-M-0534 proof execution

This module closes the frozen long exact homology sequence target with the three
exactness theorems from the pinned mathlib homology-sequence implementation.
-/

universe v u w

namespace Stage1Instances.THM_M_0534.Proof

open CategoryTheory
open CategoryTheory.Limits
open HomologicalComplex
open Stage1Instances.THM_M_0534

/-- A short exact sequence of homological complexes induces exactness at all
three repeating positions of its degree-indexed homology sequence. -/
theorem longExactHomologySequence :
    LongExactHomologySequenceTarget.{v, u, w} := by
  intro C _ _ iota c S hS
  refine ⟨?_, ?_⟩
  · intro i
    exact hS.homology_exact₂ i
  · intro i j hij
    exact ⟨hS.homology_exact₃ i j hij, hS.homology_exact₁ i j hij⟩

/-- The same proof factored through the composition node frozen by the
obligation tree. -/
theorem longExactHomologySequence_via_families :
    LongExactHomologySequenceTarget.{v, u, w} := by
  apply ObligationTree.root_of_exactness_families
  · intro C _ _ iota c S hS i
    exact hS.homology_exact₂ i
  · intro C _ _ iota c S hS i j hij
    exact hS.homology_exact₃ i j hij
  · intro C _ _ iota c S hS i j hij
    exact hS.homology_exact₁ i j hij

#print axioms longExactHomologySequence
#print axioms longExactHomologySequence_via_families

end Stage1Instances.THM_M_0534.Proof
