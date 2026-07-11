import Statement

/-!
# THM-M-0001 independent validation probe

This module reconstructs the canonical wrapper without importing `Proof`.
It is an implementation-diverse local probe, not a distinct-runner attestation.
-/

universe v u w

namespace Stage1Instances.THM_M_0001.Validation

open CategoryTheory CategoryTheory.Limits HomologicalComplex
open Stage1Instances.THM_M_0001

/-- Independent local reconstruction through the checked grouped transport. -/
theorem independentlyReconstructedLongExactHomologySequence :
    LongExactHomologySequenceTarget.{v, u, w} :=
  longExactHomologySequenceTarget_iff_grouped.mpr (by
    intro C _ _ ι c S hS
    exact
      ⟨fun i => hS.homology_exact₂ i,
       fun i j hij => hS.homology_exact₃ i j hij,
       fun i j hij => hS.homology_exact₁ i j hij⟩)

#print axioms independentlyReconstructedLongExactHomologySequence
#print axioms CategoryTheory.ShortComplex.ShortExact.homology_exact₁
#print axioms CategoryTheory.ShortComplex.ShortExact.homology_exact₂
#print axioms CategoryTheory.ShortComplex.ShortExact.homology_exact₃

end Stage1Instances.THM_M_0001.Validation
