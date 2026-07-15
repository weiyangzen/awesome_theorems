import Statement

/-!
# Checked boundary case for THM-M-0594

This module checks the empty-source case of the exact unrestricted target.
It is proof progress only: it does not close a frozen proof-graph obligation
or construct an embedding when the source manifold is inhabited.
-/

noncomputable section

open Function Topology
open scoped Manifold ContDiff

namespace Stage1Instances.THM_M_0594

universe uE uH uM

/-- The exact Whitney target is immediate when the source manifold is empty. -/
theorem whitneyEmbeddingTarget_of_isEmpty
    (E : Type uE) [NormedAddCommGroup E] [NormedSpace ℝ E]
    [FiniteDimensional ℝ E]
    (H : Type uH) [TopologicalSpace H]
    (I : ModelWithCorners ℝ E H)
    (M : Type uM) [TopologicalSpace M] [ChartedSpace H M]
    [IsManifold I ∞ M] [T2Space M] [SecondCountableTopology M]
    [BoundarylessManifold I M] [IsEmpty M] :
    WhitneyEmbeddingTarget E H I M := by
  let e : M → EuclideanSpace ℝ (Fin 0) := isEmptyElim
  refine ⟨0, e, contMDiff_of_locally_contMDiffOn (fun x => isEmptyElim x), ?_, ?_⟩
  · exact IsEmbedding.of_subsingleton e
  · intro x
    exact isEmptyElim x

#print axioms whitneyEmbeddingTarget_of_isEmpty

end Stage1Instances.THM_M_0594
