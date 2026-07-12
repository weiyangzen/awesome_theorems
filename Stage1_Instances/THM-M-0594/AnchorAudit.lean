import Mathlib.Geometry.Manifold.WhitneyEmbedding

/-!
# Checked anchor audit for THM-M-0594

The only terminal theorem found in pinned mathlib is the compact specialization.
This file checks both its exact upstream type and its relationship to the frozen
unrestricted target. It deliberately does not produce the unrestricted root.
-/

noncomputable section

open Function Topology
open scoped Manifold ContDiff

namespace Stage1Instances.THM_M_0594

universe uE uH uM

/-- The pinned compact theorem closes the frozen target only after adding `CompactSpace M`. -/
theorem compactSpecialization_of_mathlib
    (E : Type uE) [NormedAddCommGroup E] [NormedSpace ℝ E]
    [FiniteDimensional ℝ E]
    (H : Type uH) [TopologicalSpace H]
    (I : ModelWithCorners ℝ E H)
    (M : Type uM) [TopologicalSpace M] [ChartedSpace H M]
    [IsManifold I ∞ M] [T2Space M] [SecondCountableTopology M]
    [BoundarylessManifold I M] [CompactSpace M] :
    ∃ (n : ℕ) (e : M → EuclideanSpace ℝ (Fin n)),
      CMDiff ∞ e ∧ IsEmbedding e ∧
        ∀ x : M, Injective (mfderiv I (𝓡 n) e x) := by
  rcases exists_embedding_euclidean_of_compact (I := I) (M := M) with
    ⟨n, e, he_smooth, he_closed, he_deriv⟩
  exact ⟨n, e, he_smooth, he_closed.isEmbedding, he_deriv⟩

#check exists_embedding_euclidean_of_compact
#print exists_embedding_euclidean_of_compact
#check compactSpecialization_of_mathlib
#print axioms compactSpecialization_of_mathlib

end Stage1Instances.THM_M_0594
