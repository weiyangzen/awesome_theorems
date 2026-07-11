import Mathlib.Geometry.Manifold.Riemannian.Basic

/-!
# Exact statement for THM-M-0170

This module only freezes and elaborates the smooth Nash isometric embedding
target.  It contains no existence proof.
-/

noncomputable section

open scoped Bundle ContDiff Manifold

namespace Stage1Instances.THM_M_0170

universe uE uM

/-- The standard finite-dimensional Euclidean target. -/
abbrev EuclideanTarget (n : ℕ) := EuclideanSpace ℝ (Fin n)

/--
`f` is a smooth embedding and its differential preserves the Riemannian inner
product at every point.  The last conjunct is the pullback-metric equality,
written pointwise because the pinned mathlib has no bundled pullback predicate
for Riemannian metrics.
-/
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

/--
Canonical Lean target for the smooth Nash isometric embedding theorem.

Using `𝓘(ℝ, E)` freezes the source as a manifold without boundary.  The
Hausdorff and second-countable hypotheses are explicit, as is smoothness of the
Riemannian metric rather than merely continuity of its fiberwise inner products.
-/
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

/-- Checked serialization of the canonical existential target. -/
theorem statement_iff
    (E : Type uE) [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E]
    (M : Type uM) [TopologicalSpace M] [ChartedSpace E M]
    [T2Space M] [SecondCountableTopology M]
    [IsManifold 𝓘(ℝ, E) ∞ M]
    [Bundle.RiemannianBundle (fun x : M => TangentSpace 𝓘(ℝ, E) x)]
    [IsContMDiffRiemannianBundle 𝓘(ℝ, E) ∞ E
      (fun x : M => TangentSpace 𝓘(ℝ, E) x)] :
    Statement E M ↔
      ∃ (n : ℕ) (f : M → EuclideanTarget n),
        IsSmoothRiemannianIsometricEmbedding (E := E) n f :=
  Iff.rfl

/-! Statement-gate mutation fixtures.  These propositions deliberately alter
one dimension of the target; the guarded examples verify that none is
definitionally the frozen `Statement`. -/

section Mutations

variable
    (E : Type uE) [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E]
    (M : Type uM) [TopologicalSpace M] [ChartedSpace E M]
    [T2Space M] [SecondCountableTopology M]
    [IsManifold 𝓘(ℝ, E) ∞ M]
    [Bundle.RiemannianBundle (fun x : M => TangentSpace 𝓘(ℝ, E) x)]
    [IsContMDiffRiemannianBundle 𝓘(ℝ, E) ∞ E
      (fun x : M => TangentSpace 𝓘(ℝ, E) x)]

def RemovedSecondCountability : Prop :=
  ∃ (n : ℕ) (f : M → EuclideanTarget n),
    IsSmoothRiemannianIsometricEmbedding (E := E) n f

def ChangedDomain (F : Type*) [NormedAddCommGroup F] [InnerProductSpace ℝ F]
    [FiniteDimensional ℝ F] : Prop :=
  ∃ f : M → F, ContMDiff 𝓘(ℝ, E) 𝓘(ℝ, F) ∞ f ∧ Topology.IsEmbedding f

def ChangedBinderScope : Prop :=
  ∃ n : ℕ, ∃ f : M → EuclideanTarget n,
    IsSmoothRiemannianIsometricEmbedding (E := E) n f

def ExcludeZeroTarget : Prop :=
  ∃ (n : ℕ) (_ : 0 < n) (f : M → EuclideanTarget n),
    IsSmoothRiemannianIsometricEmbedding (E := E) n f

#guard_msgs (drop error) in
example : Statement E M = RemovedSecondCountability E M := rfl

#guard_msgs (drop error) in
example : Statement E M = ChangedDomain E M (EuclideanTarget 1) := rfl

#guard_msgs (drop error) in
example : Statement E M = ChangedBinderScope E M := rfl

#guard_msgs (drop error) in
example : Statement E M = ExcludeZeroTarget E M := rfl

end Mutations

end Stage1Instances.THM_M_0170

#check @Stage1Instances.THM_M_0170.Statement
#print Stage1Instances.THM_M_0170.Statement
#print axioms Stage1Instances.THM_M_0170.statement_iff
