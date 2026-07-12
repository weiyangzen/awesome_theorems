import Mathlib.Geometry.Manifold.WhitneyEmbedding

/-!
# Exact statement for THM-M-0594

This file freezes the unrestricted, existence-only Whitney embedding target.
It deliberately does not use the compactness hypothesis of mathlib's current
`exists_embedding_euclidean_of_compact` theorem.
-/

noncomputable section

open Function Topology
open scoped Manifold ContDiff

namespace Stage1Instances.THM_M_0594

universe uE uH uM

/--
Every finite-dimensional, Hausdorff, second-countable, boundaryless smooth
real manifold admits a smooth embedding into some finite-dimensional real
Euclidean space.

The conclusion spells out "smooth embedding": global smoothness, a
topological embedding, and injectivity of the manifold derivative everywhere.
No target-dimension bound and no compactness hypothesis are imposed.
-/
def WhitneyEmbeddingTarget
    (E : Type uE) [NormedAddCommGroup E] [NormedSpace ℝ E]
    [FiniteDimensional ℝ E]
    (H : Type uH) [TopologicalSpace H]
    (I : ModelWithCorners ℝ E H)
    (M : Type uM) [TopologicalSpace M] [ChartedSpace H M]
    [IsManifold I ∞ M] [T2Space M] [SecondCountableTopology M]
    [BoundarylessManifold I M] : Prop :=
  ∃ (n : ℕ) (e : M → EuclideanSpace ℝ (Fin n)),
    CMDiff ∞ e ∧ IsEmbedding e ∧
      ∀ x : M, Injective (mfderiv I (𝓡 n) e x)

/-- Checked expansion of the canonical target; this is statement identity, not a proof. -/
theorem whitneyEmbeddingTarget_iff_expanded
    (E : Type uE) [NormedAddCommGroup E] [NormedSpace ℝ E]
    [FiniteDimensional ℝ E]
    (H : Type uH) [TopologicalSpace H]
    (I : ModelWithCorners ℝ E H)
    (M : Type uM) [TopologicalSpace M] [ChartedSpace H M]
    [IsManifold I ∞ M] [T2Space M] [SecondCountableTopology M]
    [BoundarylessManifold I M] :
    WhitneyEmbeddingTarget E H I M ↔
      ∃ (n : ℕ) (e : M → EuclideanSpace ℝ (Fin n)),
        CMDiff ∞ e ∧ IsEmbedding e ∧
          ∀ x : M, Injective (mfderiv I (𝓡 n) e x) :=
  Iff.rfl

#check WhitneyEmbeddingTarget
#print WhitneyEmbeddingTarget

end Stage1Instances.THM_M_0594
