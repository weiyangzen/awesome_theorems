import Mathlib.Topology.Algebra.Module.LocallyConvex

/-!
# THM-M-0321: exact Markov-Kakutani statement

This module freezes the statement boundary only. It does not prove the
Markov-Kakutani fixed-point theorem.
-/

open Set

namespace Stage1Instances.THM_M_0321

universe u v

/-- `f` preserves real affine combinations of pairs of points in `K`.
Only combinations whose coefficients are nonnegative and sum to one are
needed, so the definition does not require the subtype `K` to be an affine
space. -/
def IsAffineOn {E : Type u} [AddCommGroup E] [Module ℝ E]
    (K : Set E) (f : E → E) : Prop :=
  ∀ x ∈ K, ∀ y ∈ K, ∀ a b : ℝ, 0 ≤ a → 0 ≤ b → a + b = 1 →
    f (a • x + b • y) = a • f x + b • f y

/-- A family has a common fixed point lying in `K`. -/
def HasCommonFixedPoint {E : Type u} {I : Type v}
    (K : Set E) (f : I → E → E) : Prop :=
  ∃ x ∈ K, ∀ i : I, f i x = x

/-- The exact Markov-Kakutani target: a pairwise commuting family of
continuous affine self-maps of a nonempty compact convex subset of a
Hausdorff locally convex real topological vector space has a common fixed
point. -/
def MarkovKakutaniTarget : Prop :=
  ∀ (E : Type u) [AddCommGroup E] [Module ℝ E] [TopologicalSpace E]
    [T2Space E] [IsTopologicalAddGroup E] [ContinuousSMul ℝ E]
    [LocallyConvexSpace ℝ E] (I : Type v) (K : Set E) (f : I → E → E),
      K.Nonempty →
      IsCompact K →
      Convex ℝ K →
      (∀ i, MapsTo (f i) K K) →
      (∀ i, ContinuousOn (f i) K) →
      (∀ i, IsAffineOn K (f i)) →
      (∀ i j, ∀ x ∈ K, f i (f j x) = f j (f i x)) →
      HasCommonFixedPoint K f

/-- An alternate spelling using `Set.EqOn` for pairwise commutation. -/
def EqOnCommutationTarget : Prop :=
  ∀ (E : Type u) [AddCommGroup E] [Module ℝ E] [TopologicalSpace E]
    [T2Space E] [IsTopologicalAddGroup E] [ContinuousSMul ℝ E]
    [LocallyConvexSpace ℝ E] (I : Type v) (K : Set E) (f : I → E → E),
      K.Nonempty → IsCompact K → Convex ℝ K →
      (∀ i, MapsTo (f i) K K) →
      (∀ i, ContinuousOn (f i) K) →
      (∀ i, IsAffineOn K (f i)) →
      (∀ i j, Set.EqOn (f i ∘ f j) (f j ∘ f i) K) →
      HasCommonFixedPoint K f

/-- Checked transport between the direct and `EqOn` commutation encodings. -/
theorem markovKakutaniTarget_iff_eqOnCommutationTarget :
    MarkovKakutaniTarget.{u, v} ↔ EqOnCommutationTarget.{u, v} := by
  rfl

-- Structural mutations: the checker verifies that none has the canonical type.
def mutationRemovedCompactness : Prop :=
  ∀ (E : Type u) [AddCommGroup E] [Module ℝ E] [TopologicalSpace E]
    [T2Space E] [IsTopologicalAddGroup E] [ContinuousSMul ℝ E]
    [LocallyConvexSpace ℝ E] (I : Type v) (K : Set E) (f : I → E → E),
      K.Nonempty → Convex ℝ K → (∀ i, MapsTo (f i) K K) →
      (∀ i, ContinuousOn (f i) K) → (∀ i, IsAffineOn K (f i)) →
      (∀ i j, ∀ x ∈ K, f i (f j x) = f j (f i x)) → HasCommonFixedPoint K f

def mutationChangedDomain : Prop :=
  ∀ (K : Set ℝ) (f : Nat → ℝ → ℝ), K.Nonempty → IsCompact K → Convex ℝ K →
    (∀ i, MapsTo (f i) K K) → (∀ i, ContinuousOn (f i) K) →
    (∀ i, IsAffineOn K (f i)) →
    (∀ i j, ∀ x ∈ K, f i (f j x) = f j (f i x)) → HasCommonFixedPoint K f

def mutationChangedBinderScope : Prop :=
  ∀ (E : Type u) [AddCommGroup E] [Module ℝ E] [TopologicalSpace E]
    [T2Space E] [IsTopologicalAddGroup E] [ContinuousSMul ℝ E]
    [LocallyConvexSpace ℝ E] (I : Type v) (K : Set E),
      K.Nonempty → IsCompact K → Convex ℝ K →
      ∃ f : I → E → E, HasCommonFixedPoint K f

def mutationNonemptyIndex : Prop :=
  ∀ (E : Type u) [AddCommGroup E] [Module ℝ E] [TopologicalSpace E]
    [T2Space E] [IsTopologicalAddGroup E] [ContinuousSMul ℝ E]
    [LocallyConvexSpace ℝ E] (I : Type v) [Nonempty I] (K : Set E) (f : I → E → E),
      K.Nonempty → IsCompact K → Convex ℝ K →
      (∀ i, MapsTo (f i) K K) → (∀ i, ContinuousOn (f i) K) →
      (∀ i, IsAffineOn K (f i)) →
      (∀ i j, ∀ x ∈ K, f i (f j x) = f j (f i x)) → HasCommonFixedPoint K f

/-- The empty-family boundary is retained: common fixed points are exactly
the points of the stipulated nonempty set. -/
theorem emptyFamily_boundary {E : Type u} (K : Set E) (f : Empty → E → E) :
    HasCommonFixedPoint K f ↔ K.Nonempty := by
  constructor
  · rintro ⟨x, hx, _⟩
    exact ⟨x, hx⟩
  · rintro ⟨x, hx⟩
    exact ⟨x, hx, fun i => i.elim⟩

end Stage1Instances.THM_M_0321

set_option pp.explicit true in
#print Stage1Instances.THM_M_0321.MarkovKakutaniTarget
