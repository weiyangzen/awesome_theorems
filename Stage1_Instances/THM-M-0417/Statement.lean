import Mathlib.MeasureTheory.Group.GeometryOfNumbers

/-!
# THM-M-0417: Minkowski convex body theorem statement

This module freezes the strict-volume form selected at intake. It declares a
proposition only; proof integration belongs to a later execution node.
-/

namespace Stage1Instances.THM_M_0417

open MeasureTheory Module

universe u

/--
The strict Minkowski convex body target, using an additive fundamental domain
whose Haar measure is the lattice covolume.
-/
def Statement : Prop :=
  ∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E]
      [MeasurableSpace E] [BorelSpace E] [FiniteDimensional ℝ E]
      (μ : Measure E) [μ.IsAddHaarMeasure]
      (L : AddSubgroup E) [Countable ↑L] (F s : Set E),
    IsAddFundamentalDomain L F μ →
      (∀ x ∈ s, -x ∈ s) →
        Convex ℝ s →
          μ F * 2 ^ finrank ℝ E < μ s →
            ∃ x ≠ 0, ((x : L) : E) ∈ s

-- Structural mutations are elaborated separately and fingerprinted by the
-- statement validator; none is an alternate target.
def mutationRemovedSymmetry : Prop :=
  ∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E]
      [MeasurableSpace E] [BorelSpace E] [FiniteDimensional ℝ E]
      (μ : Measure E) [μ.IsAddHaarMeasure]
      (L : AddSubgroup E) [Countable ↑L] (F s : Set E),
    IsAddFundamentalDomain L F μ → Convex ℝ s →
      μ F * 2 ^ finrank ℝ E < μ s →
        ∃ x ≠ 0, ((x : L) : E) ∈ s

def mutationRemovedConvexity : Prop :=
  ∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E]
      [MeasurableSpace E] [BorelSpace E] [FiniteDimensional ℝ E]
      (μ : Measure E) [μ.IsAddHaarMeasure]
      (L : AddSubgroup E) [Countable ↑L] (F s : Set E),
    IsAddFundamentalDomain L F μ → (∀ x ∈ s, -x ∈ s) →
      μ F * 2 ^ finrank ℝ E < μ s →
        ∃ x ≠ 0, ((x : L) : E) ∈ s

def mutationNonStrictThreshold : Prop :=
  ∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E]
      [MeasurableSpace E] [BorelSpace E] [FiniteDimensional ℝ E]
      (μ : Measure E) [μ.IsAddHaarMeasure]
      (L : AddSubgroup E) [Countable ↑L] (F s : Set E),
    IsAddFundamentalDomain L F μ → (∀ x ∈ s, -x ∈ s) → Convex ℝ s →
      μ F * 2 ^ finrank ℝ E ≤ μ s →
        ∃ x ≠ 0, ((x : L) : E) ∈ s

def mutationAllowsZeroWitness : Prop :=
  ∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E]
      [MeasurableSpace E] [BorelSpace E] [FiniteDimensional ℝ E]
      (μ : Measure E) [μ.IsAddHaarMeasure]
      (L : AddSubgroup E) [Countable ↑L] (F s : Set E),
    IsAddFundamentalDomain L F μ → (∀ x ∈ s, -x ∈ s) → Convex ℝ s →
      μ F * 2 ^ finrank ℝ E < μ s →
        ∃ x : L, ((x : L) : E) ∈ s

-- This annotation checks the canonical binder order and expression directly
-- against the declaration exported by the sole imported mathlib module.
#check (MeasureTheory.exists_ne_zero_mem_lattice_of_measure_mul_two_pow_lt_measure :
  ∀ {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
      [MeasurableSpace E] [BorelSpace E] [FiniteDimensional ℝ E]
      {μ : Measure E} [μ.IsAddHaarMeasure]
      {L : AddSubgroup E} [Countable ↑L] {F s : Set E},
    IsAddFundamentalDomain L F μ →
      (∀ x ∈ s, -x ∈ s) →
        Convex ℝ s →
          μ F * 2 ^ finrank ℝ E < μ s →
            ∃ x ≠ 0, ((x : L) : E) ∈ s)

end Stage1Instances.THM_M_0417

set_option pp.explicit true in
#print Stage1Instances.THM_M_0417.Statement

set_option pp.explicit true in
#print Stage1Instances.THM_M_0417.mutationRemovedSymmetry

set_option pp.explicit true in
#print Stage1Instances.THM_M_0417.mutationRemovedConvexity

set_option pp.explicit true in
#print Stage1Instances.THM_M_0417.mutationNonStrictThreshold

set_option pp.explicit true in
#print Stage1Instances.THM_M_0417.mutationAllowsZeroWitness
