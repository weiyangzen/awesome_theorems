import Mathlib.Probability.Independence.Process.HasIndepIncrements
import Mathlib.Probability.IdentDistrib

/-!
# THM-M-1070: exact Levy-process statement

This module freezes the standard real-valued Levy-process predicate on nonnegative real time.
Cadlag regularity is not built into the predicate: it belongs to the separate regularization
theorem. This file checks only the statement boundary and supplies no such regularization proof.
-/

open Filter MeasureTheory
open scoped NNReal Topology

namespace Stage1Instances.THM_M_1070

open ProbabilityTheory

/-- A real-valued process on nonnegative real time is a Levy process when it consists of
measurable random variables, starts at zero almost surely, has jointly independent and stationary
increments, and is stochastically continuous. -/
def IsLevyProcess {Ω : Type*} [MeasurableSpace Ω] (P : Measure Ω)
    (X : ℝ≥0 → Ω → ℝ) : Prop :=
  IsProbabilityMeasure P ∧
  (∀ t, AEMeasurable (X t) P) ∧
  X 0 =ᵐ[P] 0 ∧
  HasIndepIncrements X P ∧
  (∀ s t, IdentDistrib (X (s + t) - X s) (X t) P P) ∧
  ∀ t, TendstoInMeasure P X (𝓝 t) (X t)

/-- The direct source shape, kept separate so elaboration checks every binder and clause. -/
def ExpandedSourceShape {Ω : Type*} [MeasurableSpace Ω] (P : Measure Ω)
    (X : ℝ≥0 → Ω → ℝ) : Prop :=
  IsProbabilityMeasure P ∧
  (∀ t : ℝ≥0, AEMeasurable (X t) P) ∧
  (∀ᵐ ω ∂P, X 0 ω = 0) ∧
  (∀ n, ∀ t : Fin (n + 1) → ℝ≥0, Monotone t →
    iIndepFun (fun (i : Fin n) ω ↦ X (t i.succ) ω - X (t i.castSucc) ω) P) ∧
  (∀ s t : ℝ≥0, IdentDistrib
    (fun ω ↦ X (s + t) ω - X s ω) (X t) P P) ∧
  ∀ t : ℝ≥0, TendstoInMeasure P X (𝓝 t) (X t)

/-- Checked transport between the canonical predicate and its clause-by-clause expansion. -/
theorem isLevyProcess_iff_expandedSourceShape {Ω : Type*} [MeasurableSpace Ω]
    (P : Measure Ω) (X : ℝ≥0 → Ω → ℝ) :
    IsLevyProcess P X ↔ ExpandedSourceShape P X := by
  rfl

-- Deliberately changed statement shapes retained for mutation review.
def mutationPairwiseIndependentIncrements {Ω : Type*} [MeasurableSpace Ω]
    (P : Measure Ω) (X : ℝ≥0 → Ω → ℝ) : Prop :=
  ∀ r s t : ℝ≥0, r ≤ s → s ≤ t →
    IndepFun (X s - X r) (X t - X s) P

def mutationDiscreteTime {Ω : Type*} [MeasurableSpace Ω]
    (P : Measure Ω) (X : ℕ → Ω → ℝ) : Prop :=
  IsProbabilityMeasure P ∧ HasIndepIncrements X P

def mutationNoStochasticContinuity {Ω : Type*} [MeasurableSpace Ω]
    (P : Measure Ω) (X : ℝ≥0 → Ω → ℝ) : Prop :=
  IsProbabilityMeasure P ∧
  (∀ t, AEMeasurable (X t) P) ∧
  X 0 =ᵐ[P] 0 ∧
  HasIndepIncrements X P ∧
  ∀ s t, IdentDistrib (X (s + t) - X s) (X t) P P

def mutationCadlagAssumed {Ω : Type*} [MeasurableSpace Ω]
    (P : Measure Ω) (X : ℝ≥0 → Ω → ℝ) : Prop :=
  IsLevyProcess P X ∧ ∀ ω, Continuous (fun t ↦ X t ω)

end Stage1Instances.THM_M_1070

set_option pp.explicit true in
#print Stage1Instances.THM_M_1070.IsLevyProcess
