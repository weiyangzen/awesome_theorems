import Mathlib.Probability.Kernel.Composition.Comp

/-!
# THM-M-1091: exact Chapman-Kolmogorov statement

This module freezes the homogeneous discrete-time transition-kernel form selected by the
repository's "semigroup property of transition probabilities" gloss. It contains statement
transports and boundary checks, but does not claim theorem-node proof credit.
-/

noncomputable section

open MeasureTheory ProbabilityTheory Set
open scoped ENNReal ProbabilityTheory

namespace Stage1Instances.THM_M_1091

universe u

/-- The Chapman-Kolmogorov semigroup law for a homogeneous discrete-time Markov kernel.
Composition is oriented so that the `m`-step kernel acts first and the `n`-step kernel second. -/
def ChapmanKolmogorovTarget : Prop :=
  ∀ (State : Type u) [MeasurableSpace State]
    (κ : Kernel State State) [IsMarkovKernel κ] (m n : Nat),
      κ ^ (m + n) = (κ ^ n) ∘ₖ (κ ^ m)

/-- The setwise integral encoding of the same homogeneous discrete-time equation. -/
def ChapmanKolmogorovIntegralTarget : Prop :=
  ∀ (State : Type u) [MeasurableSpace State]
    (κ : Kernel State State) [IsMarkovKernel κ] (m n : Nat)
    (x : State) (A : Set State),
      MeasurableSet A →
        (κ ^ (m + n)) x A = ∫⁻ y, (κ ^ n) y A ∂((κ ^ m) x)

/-- Checked transport between kernel equality and the conventional setwise integral equation. -/
theorem target_iff_integralTarget :
    ChapmanKolmogorovTarget.{u} ↔ ChapmanKolmogorovIntegralTarget.{u} := by
  constructor
  · intro h State _ κ _ m n x A hA
    rw [h State κ m n]
    exact Kernel.comp_apply' (κ ^ n) (κ ^ m) x hA
  · intro h State _ κ _ m n
    ext x A hA
    rw [h State κ m n x A hA]
    exact (Kernel.comp_apply' (κ ^ n) (κ ^ m) x hA).symm

-- Separately elaborated structural mutations used by `check_statement.py`.
def mutationRemovedMarkovHypothesis : Prop :=
  ∀ (State : Type u) [MeasurableSpace State]
    (κ : Kernel State State) (m n : Nat),
      κ ^ (m + n) = (κ ^ n) ∘ₖ (κ ^ m)

def mutationFiniteStateDomain : Prop :=
  ∀ (cardinality : Nat) (κ : Kernel (Fin cardinality) (Fin cardinality))
    [IsMarkovKernel κ] (m n : Nat),
      κ ^ (m + n) = (κ ^ n) ∘ₖ (κ ^ m)

def mutationChangedBinderScope : Prop :=
  ∀ (State : Type u) [MeasurableSpace State]
    (κ : Kernel State State) [IsMarkovKernel κ] (m : Nat),
      (∀ n : Nat, κ ^ (n + m) = (κ ^ n) ∘ₖ (κ ^ m))

def mutationPositiveStepsOnly : Prop :=
  ∀ (State : Type u) [MeasurableSpace State]
    (κ : Kernel State State) [IsMarkovKernel κ] (m n : Nat),
      0 < m → 0 < n → κ ^ (m + n) = (κ ^ n) ∘ₖ (κ ^ m)

/-- The zero-first-step boundary reduces to the identity kernel. -/
theorem zero_first_step_boundary
    (State : Type u) [MeasurableSpace State]
    (κ : Kernel State State) [IsMarkovKernel κ] (n : Nat) :
    κ ^ (0 + n) = (κ ^ n) ∘ₖ (κ ^ 0) := by
  simpa only [zero_add, pow_zero] using (Kernel.comp_id (κ ^ n)).symm

/-- The zero-second-step boundary reduces to the identity kernel. -/
theorem zero_second_step_boundary
    (State : Type u) [MeasurableSpace State]
    (κ : Kernel State State) [IsMarkovKernel κ] (m : Nat) :
    κ ^ (m + 0) = (κ ^ 0) ∘ₖ (κ ^ m) := by
  simpa only [add_zero, pow_zero] using (Kernel.id_comp (κ ^ m)).symm

end Stage1Instances.THM_M_1091

set_option pp.explicit true in
#print Stage1Instances.THM_M_1091.ChapmanKolmogorovTarget
