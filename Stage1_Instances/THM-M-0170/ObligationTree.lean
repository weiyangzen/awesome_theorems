import Mathlib.Geometry.Manifold.Riemannian.Basic

/-!
# THM-M-0170 conditional branch composition

This checks only the exhaustive compact/noncompact recomposition of the frozen
target. The two branch packages are explicit premises; this file supplies no
Nash embedding construction.
-/

noncomputable section

open scoped Bundle ContDiff Manifold

namespace Stage1Instances.THM_M_0170

universe uE uM

abbrev EuclideanTarget (n : ℕ) := EuclideanSpace ℝ (Fin n)

def IsSmoothRiemannianIsometricEmbedding
    {E : Type uE} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    {M : Type uM} [TopologicalSpace M] [ChartedSpace E M]
    [Bundle.RiemannianBundle (fun x : M => TangentSpace 𝓘(ℝ, E) x)]
    (n : ℕ) (f : M → EuclideanTarget n) : Prop :=
  ContMDiff 𝓘(ℝ, E) 𝓘(ℝ, EuclideanTarget n) ∞ f ∧ Topology.IsEmbedding f ∧
    ∀ (x : M) (v w : TangentSpace 𝓘(ℝ, E) x),
      inner ℝ (mfderiv 𝓘(ℝ, E) 𝓘(ℝ, EuclideanTarget n) f x v)
          (mfderiv 𝓘(ℝ, E) 𝓘(ℝ, EuclideanTarget n) f x w) = inner ℝ v w

def Statement
    (E : Type uE) [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E]
    (M : Type uM) [TopologicalSpace M] [ChartedSpace E M]
    [T2Space M] [SecondCountableTopology M] [IsManifold 𝓘(ℝ, E) ∞ M]
    [Bundle.RiemannianBundle (fun x : M => TangentSpace 𝓘(ℝ, E) x)]
    [IsContMDiffRiemannianBundle 𝓘(ℝ, E) ∞ E
      (fun x : M => TangentSpace 𝓘(ℝ, E) x)] : Prop :=
  ∃ (n : ℕ) (f : M → EuclideanTarget n),
    IsSmoothRiemannianIsometricEmbedding (E := E) n f

def CompactPackage : Prop :=
  ∀ (E : Type uE) [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E]
    (M : Type uM) [TopologicalSpace M] [ChartedSpace E M]
    [T2Space M] [SecondCountableTopology M]
    [IsManifold 𝓘(ℝ, E) ∞ M]
    [Bundle.RiemannianBundle (fun x : M => TangentSpace 𝓘(ℝ, E) x)]
    [IsContMDiffRiemannianBundle 𝓘(ℝ, E) ∞ E
      (fun x : M => TangentSpace 𝓘(ℝ, E) x)],
    Nonempty (CompactSpace M) → Statement E M

def NoncompactPackage : Prop :=
  ∀ (E : Type uE) [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E]
    (M : Type uM) [TopologicalSpace M] [ChartedSpace E M]
    [T2Space M] [SecondCountableTopology M]
    [IsManifold 𝓘(ℝ, E) ∞ M]
    [Bundle.RiemannianBundle (fun x : M => TangentSpace 𝓘(ℝ, E) x)]
    [IsContMDiffRiemannianBundle 𝓘(ℝ, E) ∞ E
      (fun x : M => TangentSpace 𝓘(ℝ, E) x)],
    ¬ Nonempty (CompactSpace M) → Statement E M

/-- Exact recomposition; neither mathematical branch is proved here. -/
theorem statement_of_compact_and_noncompact
    (compact : CompactPackage.{uE, uM})
    (noncompact : NoncompactPackage.{uE, uM}) :
    ∀ (E : Type uE) [NormedAddCommGroup E] [InnerProductSpace ℝ E]
      [FiniteDimensional ℝ E]
      (M : Type uM) [TopologicalSpace M] [ChartedSpace E M]
      [T2Space M] [SecondCountableTopology M]
      [IsManifold 𝓘(ℝ, E) ∞ M]
      [Bundle.RiemannianBundle (fun x : M => TangentSpace 𝓘(ℝ, E) x)]
      [IsContMDiffRiemannianBundle 𝓘(ℝ, E) ∞ E
        (fun x : M => TangentSpace 𝓘(ℝ, E) x)],
      Statement E M := by
  intro E _ _ _ M _ _ _ _ _ _ _
  classical
  by_cases h : Nonempty (CompactSpace M)
  · exact compact E M h
  · exact noncompact E M h

#print axioms statement_of_compact_and_noncompact

end Stage1Instances.THM_M_0170
