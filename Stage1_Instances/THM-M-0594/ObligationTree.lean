import Statement

/-!
# THM-M-0594 conditional obligation composition

This module checks the final constructor selected by the frozen architecture.
It consumes an explicit smooth embedding witness and does not construct one.
-/

noncomputable section

open Function Topology
open scoped Manifold ContDiff

namespace Stage1Instances.THM_M_0594

universe uE uH uM

/-- Checked final composition from the architecture's explicit witness package. -/
theorem root_of_smooth_embedding_witness
    (E : Type uE) [NormedAddCommGroup E] [NormedSpace ℝ E]
    [FiniteDimensional ℝ E]
    (H : Type uH) [TopologicalSpace H]
    (I : ModelWithCorners ℝ E H)
    (M : Type uM) [TopologicalSpace M] [ChartedSpace H M]
    [IsManifold I ∞ M] [T2Space M] [SecondCountableTopology M]
    [BoundarylessManifold I M]
    (n : ℕ) (e : M → EuclideanSpace ℝ (Fin n))
    (smooth : CMDiff ∞ e) (embedding : IsEmbedding e)
    (immersion : ∀ x : M, Injective (mfderiv I (𝓡 n) e x)) :
    WhitneyEmbeddingTarget E H I M :=
  ⟨n, e, smooth, embedding, immersion⟩

#print axioms root_of_smooth_embedding_witness

end Stage1Instances.THM_M_0594
