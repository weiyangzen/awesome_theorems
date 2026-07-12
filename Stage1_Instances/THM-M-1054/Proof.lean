import ObligationTree

/-!
# THM-M-1054 proof bodies

This module instantiates the frozen nontrivial mean-ergodic package with the
pinned mathlib theorem and then uses the previously checked branch assembly to
prove the exact intake-selected root.
-/

noncomputable section

open Filter MeasureTheory
open scoped ENNReal Topology

namespace Stage1Instances.THM_M_1054

universe u

/-- The nontrivial branch is exactly mathlib's Hilbert-space mean-ergodic
theorem, specialized to the Koopman contraction on real `L^2`. -/
theorem nontrivialMeanErgodicPackage_proof :
    NontrivialMeanErgodicPackage.{u} := by
  intro Omega _ mu _ T hT f _ contraction
  exact ContinuousLinearMap.tendsto_birkhoffAverage_orthogonalProjection
    (Koopman T hT) contraction f

/-- The exact frozen von Neumann `L^2` mean-ergodic target. The assembly
theorem supplies the subsingleton branch and Koopman contractivity. -/
theorem vonNeumannL2MeanErgodic :
    VonNeumannL2MeanErgodicTarget.{u} :=
  root_of_nontrivialMeanErgodicPackage nontrivialMeanErgodicPackage_proof

#print axioms nontrivialMeanErgodicPackage_proof
#print axioms vonNeumannL2MeanErgodic

end Stage1Instances.THM_M_1054
