import Statement

/-!
# THM-M-0009: proof of the long exact Ext sequence target

The canonical wrapper closes both universally indexed variance branches using
the exactness theorems from the pinned mathlib dependency.
-/

universe w v u

namespace Stage1Instances.THM_M_0009.Proof

open CategoryTheory
open Stage1Instances.THM_M_0009

/-- Every short exact sequence in either argument induces the corresponding
long exact Ext sequence at every pair of successive natural degrees. -/
theorem longExactExtSequence :
    LongExactExtSequenceTarget.{w, v, u} := by
  intro C _ _ _
  constructor
  · intro X S hS n₀ n₁ h
    exact Abelian.Ext.covariantSequence_exact X hS n₀ n₁ h
  · intro Y S hS n₀ n₁ h
    exact Abelian.Ext.contravariantSequence_exact hS Y n₀ n₁ h

#print axioms longExactExtSequence

end Stage1Instances.THM_M_0009.Proof
