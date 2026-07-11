import Statement

/-!
# THM-M-0001: proof of the long exact homology sequence target

The proof imports the exact frozen target through an isolated, temporary
`Statement.olean` built by `check_proof.sh`.
-/

universe v u w

namespace Stage1Instances.THM_M_0001.Proof

open CategoryTheory CategoryTheory.Limits HomologicalComplex
open Stage1Instances.THM_M_0001

/-- A short exact sequence of homological complexes induces exactness at all
three repeating positions of its degree-indexed homology sequence. -/
theorem longExactHomologySequence :
    LongExactHomologySequenceTarget.{v, u, w} := by
  intro C _ _ ι c S hS
  refine ⟨?_, ?_⟩
  · intro i
    exact hS.homology_exact₂ i
  · intro i j hij
    exact ⟨hS.homology_exact₃ i j hij, hS.homology_exact₁ i j hij⟩

#print axioms longExactHomologySequence

end Stage1Instances.THM_M_0001.Proof
