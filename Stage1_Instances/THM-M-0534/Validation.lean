import Statement

/-!
# THM-M-0534 independent validation probe

This module reconstructs the exact frozen root without importing `Proof` or
`ObligationTree`. It deliberately applies the three pinned mathlib exactness
theorems again so that validation is not merely an alias of the proof-phase
wrapper.
-/

universe v u w

namespace Stage1Instances.THM_M_0534.Validation

open CategoryTheory
open CategoryTheory.Limits
open HomologicalComplex
open Stage1Instances.THM_M_0534

/-- An independently implemented reconstruction of the exact frozen root. -/
theorem independentlyReconstructedLongExactHomologySequence :
    LongExactHomologySequenceTarget.{v, u, w} := by
  intro C _ _ iota c S hS
  constructor
  · exact hS.homology_exact₂
  · intro i j hij
    constructor
    · exact hS.homology_exact₃ i j hij
    · exact hS.homology_exact₁ i j hij

#print axioms independentlyReconstructedLongExactHomologySequence

end Stage1Instances.THM_M_0534.Validation
