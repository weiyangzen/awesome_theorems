import Mathlib.Geometry.Manifold.Riemannian.Basic
import Mathlib.Geometry.Manifold.WhitneyEmbedding

/-!
# Kernel probes for the THM-M-0170 anchor audit

These probes check the nearby pinned mathlib substrate.  They deliberately do
not state or prove the Nash existence theorem.
-/

noncomputable section

open scoped Bundle ContDiff Manifold

namespace Stage1Instances.THM_M_0170.AnchorAudit

universe uE uM

/-- Exact checked wrapper for mathlib's compact Whitney candidate. -/
theorem compactWhitneyCandidate
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
    [FiniteDimensional ℝ E]
    {M : Type uM} [TopologicalSpace M] [ChartedSpace E M]
    [IsManifold 𝓘(ℝ, E) ∞ M] [T2Space M] [CompactSpace M] :
    ∃ (n : ℕ) (f : M → EuclideanSpace ℝ (Fin n)),
      ContMDiff 𝓘(ℝ, E) 𝓘(ℝ, EuclideanSpace ℝ (Fin n)) ∞ f ∧
        Topology.IsClosedEmbedding f ∧
        ∀ x : M, Function.Injective
          (mfderiv 𝓘(ℝ, E) 𝓘(ℝ, EuclideanSpace ℝ (Fin n)) f x) :=
  exists_embedding_euclidean_of_compact (I := 𝓘(ℝ, E)) (M := M)

end Stage1Instances.THM_M_0170.AnchorAudit

#check @exists_embedding_euclidean_of_compact
#check @Stage1Instances.THM_M_0170.AnchorAudit.compactWhitneyCandidate
#print axioms Stage1Instances.THM_M_0170.AnchorAudit.compactWhitneyCandidate
