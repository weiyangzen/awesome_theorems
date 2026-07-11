import Statement

/-!
# THM-M-0009 independent local validation probe

This module reconstructs the canonical theorem through the checked variance
transport without importing `Proof`. It is implementation-diverse local
evidence, not a distinct-runner attestation.
-/

universe w v u

namespace Stage1Instances.THM_M_0009.Validation

open CategoryTheory
open Stage1Instances.THM_M_0009

/-- A second local construction of the exact frozen target, deliberately using
the checked transport rather than the proof phase's direct conjunction. -/
theorem independentlyReconstructedLongExactExtSequence :
    LongExactExtSequenceTarget.{w, v, u} :=
  longExactExtSequenceTarget_iff_variance_branches.mpr ⟨by
    intro C _ _ _ X S hS n₀ n₁ h
    exact Abelian.Ext.covariantSequence_exact X hS n₀ n₁ h, by
    intro C _ _ _ Y S hS n₀ n₁ h
    exact Abelian.Ext.contravariantSequence_exact hS Y n₀ n₁ h⟩

#print axioms independentlyReconstructedLongExactExtSequence
#print axioms Abelian.Ext.covariantSequence_exact
#print axioms Abelian.Ext.contravariantSequence_exact

end Stage1Instances.THM_M_0009.Validation
