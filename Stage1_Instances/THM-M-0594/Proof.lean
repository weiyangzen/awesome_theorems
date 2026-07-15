import Statement
import ProofSupport
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0594 partial proof execution

This module closes the frozen proper-injective-to-embedding bridge and checks
its composition into the exact root. The finite-dimensional global map with
smoothness, injectivity, properness, and injective manifold derivative remains
an explicit premise, so this is not a proof of the unrestricted Whitney root.
-/

noncomputable section

open Function Topology
open scoped Manifold ContDiff

namespace Stage1Instances.THM_M_0594

universe uE uH uM

/-- Frozen obligation `M0594-L-TOPOLOGICAL`: properness and point separation
upgrade the constructed Euclidean map to a topological embedding. -/
theorem properInjectiveEuclideanMap_isEmbedding
    {M : Type uM} [TopologicalSpace M]
    {n : ℕ} {e : M → EuclideanSpace ℝ (Fin n)}
    (proper : IsProperMap e) (injective : Injective e) :
    IsEmbedding e :=
  isEmbedding_of_isProperMap_of_injective proper injective

/-- Exact-root composition after the topological bridge is discharged. The
premises still expose the open global noncompact construction package. -/
theorem whitneyEmbeddingTarget_of_properInjectiveImmersion
    (E : Type uE) [NormedAddCommGroup E] [NormedSpace ℝ E]
    [FiniteDimensional ℝ E]
    (H : Type uH) [TopologicalSpace H]
    (I : ModelWithCorners ℝ E H)
    (M : Type uM) [TopologicalSpace M] [ChartedSpace H M]
    [IsManifold I ∞ M] [T2Space M] [SecondCountableTopology M]
    [BoundarylessManifold I M]
    (n : ℕ) (e : M → EuclideanSpace ℝ (Fin n))
    (smooth : CMDiff ∞ e) (proper : IsProperMap e)
    (injective : Injective e)
    (immersion : ∀ x : M, Injective (mfderiv I (𝓡 n) e x)) :
    WhitneyEmbeddingTarget E H I M :=
  ⟨n, e, smooth,
    properInjectiveEuclideanMap_isEmbedding proper injective,
    immersion⟩

assert_no_sorry properInjectiveEuclideanMap_isEmbedding
assert_no_sorry whitneyEmbeddingTarget_of_properInjectiveImmersion

#print sorries properInjectiveEuclideanMap_isEmbedding
#print sorries whitneyEmbeddingTarget_of_properInjectiveImmersion

#print axioms properInjectiveEuclideanMap_isEmbedding
#print axioms whitneyEmbeddingTarget_of_properInjectiveImmersion

end Stage1Instances.THM_M_0594
