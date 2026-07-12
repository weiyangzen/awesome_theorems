import Statement
import ObligationTree

/-!
# THM-M-1012 proof phase

This module closes the frozen machine proof cut using the exact Levy continuity theorem from the
pinned mathlib dependency.  The two directions are projected separately and then recomposed through
the frozen obligation-tree interface before the exact statement target is inhabited.
-/

noncomputable section

open Filter MeasureTheory
open scoped Topology RealInnerProductSpace

namespace Stage1Instances.THM_M_1012.Proof

open Stage1Instances.THM_M_1012

universe u

/-- Exact pinned proof of the forward characteristic-function implication. -/
theorem pinnedForward : ObligationTree.ForwardTarget.{u} := by
  intro E _ _ _ _ _ mu mu0 hmu t
  exact (ProbabilityMeasure.tendsto_iff_tendsto_charFun (μ := mu) (μ₀ := mu0)).mp hmu t

/-- Exact pinned proof of the reverse weak-convergence implication. -/
theorem pinnedReverse : ObligationTree.ReverseTarget.{u} := by
  intro E _ _ _ _ _ mu mu0 hchar
  exact (ProbabilityMeasure.tendsto_iff_tendsto_charFun (μ := mu) (μ₀ := mu0)).mpr hchar

/-- Child-to-parent composition through the interface frozen before proof execution. -/
theorem assembledObligationRoot : ObligationTree.RootTarget.{u} :=
  ObligationTree.root_of_directions pinnedForward pinnedReverse

/-- Placeholder-free proof of the canonical proposition frozen in `Statement.lean`. -/
theorem levyContinuityKnownLimit : LevyContinuityKnownLimitTarget.{u} :=
  assembledObligationRoot

#print axioms pinnedForward
#print axioms pinnedReverse
#print axioms assembledObligationRoot
#print axioms levyContinuityKnownLimit

end Stage1Instances.THM_M_1012.Proof
