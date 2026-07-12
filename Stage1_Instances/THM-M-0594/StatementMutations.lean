import Statement

/-!
Negative statement-identity tests. Each `rfl` must fail: the mutations remove a
source hypothesis, add compactness, fix an unjustified dimension bound, or
weaken smooth embedding to a continuous injection.
-/

open Function Module Topology
open scoped Manifold ContDiff

namespace Stage1Instances.THM_M_0594.Mutations

universe uE uH uM

def RemovedSecondCountability
    (E : Type uE) [NormedAddCommGroup E] [NormedSpace ℝ E]
    [FiniteDimensional ℝ E]
    (H : Type uH) [TopologicalSpace H]
    (I : ModelWithCorners ℝ E H)
    (M : Type uM) [TopologicalSpace M] [ChartedSpace H M]
    [IsManifold I ∞ M] [T2Space M] [BoundarylessManifold I M] : Prop :=
  ∃ (n : ℕ) (e : M → EuclideanSpace ℝ (Fin n)),
    CMDiff ∞ e ∧ IsEmbedding e ∧
      ∀ x : M, Injective (mfderiv I (𝓡 n) e x)

example : @WhitneyEmbeddingTarget = @RemovedSecondCountability := rfl

def AddedCompactness
    (E : Type uE) [NormedAddCommGroup E] [NormedSpace ℝ E]
    [FiniteDimensional ℝ E]
    (H : Type uH) [TopologicalSpace H]
    (I : ModelWithCorners ℝ E H)
    (M : Type uM) [TopologicalSpace M] [ChartedSpace H M]
    [IsManifold I ∞ M] [T2Space M] [SecondCountableTopology M]
    [BoundarylessManifold I M] [CompactSpace M] : Prop :=
  ∃ (n : ℕ) (e : M → EuclideanSpace ℝ (Fin n)),
    CMDiff ∞ e ∧ IsEmbedding e ∧
      ∀ x : M, Injective (mfderiv I (𝓡 n) e x)

example : @WhitneyEmbeddingTarget = @AddedCompactness := rfl

def FixedWeakDimensionBound
    (E : Type uE) [NormedAddCommGroup E] [NormedSpace ℝ E]
    [FiniteDimensional ℝ E]
    (H : Type uH) [TopologicalSpace H]
    (I : ModelWithCorners ℝ E H)
    (M : Type uM) [TopologicalSpace M] [ChartedSpace H M]
    [IsManifold I ∞ M] [T2Space M] [SecondCountableTopology M]
    [BoundarylessManifold I M] : Prop :=
  ∃ e : M → EuclideanSpace ℝ (Fin (2 * finrank ℝ E + 1)),
    ContMDiff I (𝓡 (2 * finrank ℝ E + 1)) ∞ e ∧ IsEmbedding e ∧
      ∀ x : M,
        Injective (mfderiv I (𝓡 (2 * finrank ℝ E + 1)) e x)

example : @WhitneyEmbeddingTarget = @FixedWeakDimensionBound := rfl

def WeakenedToContinuousInjection
    (E : Type uE) [NormedAddCommGroup E] [NormedSpace ℝ E]
    [FiniteDimensional ℝ E]
    (H : Type uH) [TopologicalSpace H]
    (I : ModelWithCorners ℝ E H)
    (M : Type uM) [TopologicalSpace M] [ChartedSpace H M]
    [IsManifold I ∞ M] [T2Space M] [SecondCountableTopology M]
    [BoundarylessManifold I M] : Prop :=
  ∃ (n : ℕ) (e : M → EuclideanSpace ℝ (Fin n)), Continuous e ∧ Injective e

example : @WhitneyEmbeddingTarget = @WeakenedToContinuousInjection := rfl

end Stage1Instances.THM_M_0594.Mutations
