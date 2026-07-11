import Mathlib.Geometry.Manifold.Riemannian.Basic

/-!
# THM-M-0170 proof execution

This module closes the empty-manifold boundary leaf of the frozen Nash
embedding obligation tree. The two central compact/noncompact branch packages
remain open; this is deliberately not a proof of the root statement.
-/

noncomputable section

open scoped Bundle ContDiff Manifold

namespace Stage1Instances.THM_M_0170.Proof

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

/-- The frozen target holds for an empty manifold, including the permitted
zero-dimensional Euclidean target. -/
theorem statement_of_isEmpty
    (E : Type uE) [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E]
    (M : Type uM) [TopologicalSpace M] [ChartedSpace E M]
    [T2Space M] [SecondCountableTopology M]
    [IsManifold 𝓘(ℝ, E) ∞ M]
    [Bundle.RiemannianBundle (fun x : M => TangentSpace 𝓘(ℝ, E) x)]
    [IsContMDiffRiemannianBundle 𝓘(ℝ, E) ∞ E
      (fun x : M => TangentSpace 𝓘(ℝ, E) x)]
    [IsEmpty M] : Statement E M := by
  let f : M → EuclideanTarget 0 := isEmptyElim
  refine ⟨0, f, ?_, ?_, ?_⟩
  · exact contMDiff_of_locally_contMDiffOn (fun x => isEmptyElim x)
  · exact (Topology.IsInducing.of_subsingleton f).isEmbedding
  · intro x
    exact isEmptyElim x

#print axioms statement_of_isEmpty

end Stage1Instances.THM_M_0170.Proof
