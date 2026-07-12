import ObligationTree

/-!
# THM-M-1141 proof-phase bodies

This module closes the positivity bookkeeping package and a finite-chain
comparison package. The analytic local-ball estimate and the construction of
uniform chains over a compact set remain explicit open obligations.
-/

open Set
open InnerProductSpace

namespace Stage1Instances.THM_M_1141

/-- Strict positivity on the domain supplies the positive, nonzero
denominators needed at every point of the compact subset. -/
theorem positive_denominators_on_compact
    {n : Nat} {Ω K : Set (Space n)} {u : Space n → Real}
    (hKΩ : K ⊆ Ω) (hupos : ∀ z ∈ Ω, 0 < u z) :
    ∀ x ∈ K, 0 < u x ∧ u x ≠ 0 := by
  intro x hx
  have hux : 0 < u x := hupos x (hKΩ hx)
  exact ⟨hux, ne_of_gt hux⟩

/-- A symmetric multiplicative comparison between two values. -/
def SymmetricComparison {α : Type*} (A : Real) (u : α → Real)
    (x y : α) : Prop :=
  u y ≤ A * u x ∧ u x ≤ A * u y

/-- A finite chain records one comparison at each successive link. The final
point is an index of the predicate so no arbitrary default endpoint is needed. -/
inductive ComparisonChain {α : Type*} (A : Real) (u : α → Real) :
    α → List α → α → Prop
  | nil (x : α) : ComparisonChain A u x [] x
  | cons {x y z : α} {tail : List α} :
      SymmetricComparison A u x y →
      ComparisonChain A u y tail z →
      ComparisonChain A u x (y :: tail) z

/-- Symmetric comparisons compose, multiplying their constants. -/
theorem SymmetricComparison.trans {α : Type*} {u : α → Real}
    {A B : Real} (hA : 0 ≤ A) (hB : 0 ≤ B) {x y z : α}
    (hxy : SymmetricComparison A u x y)
    (hyz : SymmetricComparison B u y z) :
    SymmetricComparison (A * B) u x z := by
  constructor
  · calc
      u z ≤ B * u y := hyz.1
      _ ≤ B * (A * u x) := mul_le_mul_of_nonneg_left hxy.1 hB
      _ = (A * B) * u x := by ring
  · calc
      u x ≤ A * u y := hxy.2
      _ ≤ A * (B * u z) := mul_le_mul_of_nonneg_left hyz.2 hA
      _ = (A * B) * u z := by ring

/-- Propagate one local constant along a finite chain. A chain with `k` links
has endpoint comparison constant `A ^ k`. -/
theorem ComparisonChain.endpoint {α : Type*} {u : α → Real}
    {A : Real} (hA : 1 ≤ A) {x z : α} {points : List α}
    (chain : ComparisonChain A u x points z) :
    SymmetricComparison (A ^ points.length) u x z := by
  induction chain with
  | nil x =>
      exact ⟨by simp, by simp⟩
  | @cons x y z tail hxy chain ih =>
      rw [List.length_cons, pow_succ']
      exact hxy.trans (by linarith) (by positivity) ih

/-- The already checked ratio transport is the exact remaining composition
once the analytic and compactness work supplies uniform value comparison. -/
theorem harnackInequality_of_analytic_package
    (comparison : UniformValueComparison) : HarnackInequality :=
  harnackInequality_of_uniformValueComparison comparison

#print axioms positive_denominators_on_compact
#print axioms ComparisonChain.endpoint
#print axioms harnackInequality_of_analytic_package

end Stage1Instances.THM_M_1141
