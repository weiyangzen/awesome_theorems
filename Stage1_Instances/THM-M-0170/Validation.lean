import Mathlib.Geometry.Manifold.Riemannian.Basic

/-!
# THM-M-0170 independent narrow validation probe

This module reconstructs the frozen target and its empty-manifold boundary
case without importing or invoking `Proof.lean`. It does not supply either
Nash construction branch.
-/

noncomputable section

open scoped Bundle ContDiff Manifold

namespace Stage1Instances.THM_M_0170.Validation

universe uE uM

abbrev EuclideanTarget (n : ℕ) := EuclideanSpace ℝ (Fin n)

def IsSmoothRiemannianIsometricEmbedding
    {E : Type uE} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    {M : Type uM} [TopologicalSpace M] [ChartedSpace E M]
    [Bundle.RiemannianBundle (fun x : M => TangentSpace 𝓘(ℝ, E) x)]
    (n : ℕ) (f : M → EuclideanTarget n) : Prop :=
  ContMDiff 𝓘(ℝ, E) 𝓘(ℝ, EuclideanTarget n) ∞ f ∧
    Topology.IsEmbedding f ∧
    ∀ (x : M) (v w : TangentSpace 𝓘(ℝ, E) x),
      inner ℝ
          (mfderiv 𝓘(ℝ, E) 𝓘(ℝ, EuclideanTarget n) f x v)
          (mfderiv 𝓘(ℝ, E) 𝓘(ℝ, EuclideanTarget n) f x w) =
        inner ℝ v w

def Statement
    (E : Type uE) [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E]
    (M : Type uM) [TopologicalSpace M] [ChartedSpace E M]
    [T2Space M] [SecondCountableTopology M]
    [IsManifold 𝓘(ℝ, E) ∞ M]
    [Bundle.RiemannianBundle (fun x : M => TangentSpace 𝓘(ℝ, E) x)]
    [IsContMDiffRiemannianBundle 𝓘(ℝ, E) ∞ E
      (fun x : M => TangentSpace 𝓘(ℝ, E) x)] : Prop :=
  ∃ (n : ℕ) (f : M → EuclideanTarget n),
    IsSmoothRiemannianIsometricEmbedding (E := E) n f

/-- A separately written kernel probe for the only proof-phase closure. -/
theorem empty_boundary_probe
    (E : Type uE) [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E]
    (M : Type uM) [TopologicalSpace M] [ChartedSpace E M]
    [T2Space M] [SecondCountableTopology M]
    [IsManifold 𝓘(ℝ, E) ∞ M]
    [Bundle.RiemannianBundle (fun x : M => TangentSpace 𝓘(ℝ, E) x)]
    [IsContMDiffRiemannianBundle 𝓘(ℝ, E) ∞ E
      (fun x : M => TangentSpace 𝓘(ℝ, E) x)]
    [IsEmpty M] : Statement E M := by
  refine ⟨0, isEmptyElim, ?_, ?_, ?_⟩
  · exact contMDiff_of_locally_contMDiffOn (fun x => isEmptyElim x)
  · exact (Topology.IsInducing.of_subsingleton isEmptyElim).isEmbedding
  · intro x
    exact isEmptyElim x

#check empty_boundary_probe
#print axioms empty_boundary_probe

end Stage1Instances.THM_M_0170.Validation
