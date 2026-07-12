import Mathlib.Analysis.SpecialFunctions.Log.ENNRealLog
import Mathlib.MeasureTheory.Integral.Lebesgue.Basic
import Mathlib.MeasureTheory.Measure.Typeclasses.Probability

/-!
# THM-M-1061: exact bounded-continuous Varadhan integral lemma statement

This module freezes and elaborates the statement boundary only. It contains no
proof of Varadhan's lemma.
-/

namespace Stage1Instances.THM_M_1061

open Filter MeasureTheory Set Topology
open scoped ENNReal

universe u

/-- A sequence of probability measures satisfies the full LDP at vanishing
positive speed `a` with rate `I`. The bounds are stated directly for every
closed and open set, avoiding reliance on an unpinned LDP interface. -/
def SatisfiesLDP {X : Type u} [MeasurableSpace X] [TopologicalSpace X]
    (μ : ℕ → Measure X) (a : ℕ → ℝ) (I : X → ℝ≥0∞) : Prop :=
  (∀ n, IsProbabilityMeasure (μ n)) ∧
  (∀ n, 0 < a n) ∧
  Tendsto a atTop (𝓝 0) ∧
  (∀ C : Set X, IsClosed C →
    limsup (fun n ↦ (a n : EReal) * ENNReal.log (μ n C)) atTop ≤
      -⨅ x ∈ C, (I x : EReal)) ∧
  (∀ G : Set X, IsOpen G →
    -⨅ x ∈ G, (I x : EReal) ≤
      liminf (fun n ↦ (a n : EReal) * ENNReal.log (μ n G)) atTop)

/-- A good rate function: lower semicontinuous with compact sublevel sets. -/
def IsGoodRateFunction {X : Type u} [TopologicalSpace X] (I : X → ℝ≥0∞) : Prop :=
  LowerSemicontinuous I ∧ ∀ r : ℝ≥0∞, r ≠ ∞ → IsCompact {x | I x ≤ r}

/-- The logarithmic exponential integral at index `n`, in `EReal` so zero and
infinite integrals retain their correct extended values. -/
noncomputable def LogExpIntegral {X : Type u} [MeasurableSpace X]
    (μ : ℕ → Measure X) (a : ℕ → ℝ) (F : X → ℝ) (n : ℕ) : EReal :=
  (a n : EReal) * ENNReal.log (∫⁻ x, ENNReal.ofReal (Real.exp (F x / a n)) ∂μ n)

/-- The bounded-continuous form of Varadhan's integral lemma selected at
intake. The ambient Polish space is nonempty, removing the empty-space
convention from the root. -/
def VaradhanIntegralLemmaTarget : Prop :=
  ∀ (X : Type u) [PseudoMetricSpace X] [CompleteSpace X]
    [SecondCountableTopology X] [MeasurableSpace X] [BorelSpace X] [Nonempty X]
    (μ : ℕ → Measure X) (a : ℕ → ℝ) (I : X → ℝ≥0∞) (F : X → ℝ),
      SatisfiesLDP μ a I →
      IsGoodRateFunction I →
      Continuous F →
      (∃ B : ℝ, ∀ x, |F x| ≤ B) →
      Tendsto (LogExpIntegral μ a F) atTop
        (𝓝 (⨆ x : X, (F x : EReal) - (I x : EReal)))

/-- Direct expansion used to check that the named root adds no assumptions. -/
def ExpandedTarget : Prop :=
  ∀ (X : Type u) [PseudoMetricSpace X] [CompleteSpace X]
    [SecondCountableTopology X] [MeasurableSpace X] [BorelSpace X] [Nonempty X]
    (μ : ℕ → Measure X) (a : ℕ → ℝ) (I : X → ℝ≥0∞) (F : X → ℝ),
      ((∀ n, IsProbabilityMeasure (μ n)) ∧
       (∀ n, 0 < a n) ∧ Tendsto a atTop (𝓝 0) ∧
       (∀ C : Set X, IsClosed C →
         limsup (fun n ↦ (a n : EReal) * ENNReal.log (μ n C)) atTop ≤
           -⨅ x ∈ C, (I x : EReal)) ∧
       (∀ G : Set X, IsOpen G →
         -⨅ x ∈ G, (I x : EReal) ≤
           liminf (fun n ↦ (a n : EReal) * ENNReal.log (μ n G)) atTop)) →
      (LowerSemicontinuous I ∧
        ∀ r : ℝ≥0∞, r ≠ ∞ → IsCompact {x | I x ≤ r}) →
      Continuous F → (∃ B : ℝ, ∀ x, |F x| ≤ B) →
      Tendsto
        (fun n ↦ (a n : EReal) *
          ENNReal.log (∫⁻ x, ENNReal.ofReal (Real.exp (F x / a n)) ∂μ n))
        atTop (𝓝 (⨆ x : X, (F x : EReal) - (I x : EReal)))

/-- Checked definitional transport to the fully expanded encoding. -/
theorem varadhanIntegralLemmaTarget_iff_expandedTarget :
    VaradhanIntegralLemmaTarget.{u} ↔ ExpandedTarget.{u} := Iff.rfl

-- Separately elaborated structural mutations for statement-boundary comparison.
def mutationRemovedGoodRate : Prop :=
  ∀ (X : Type u) [PseudoMetricSpace X] [CompleteSpace X]
    [SecondCountableTopology X] [MeasurableSpace X] [BorelSpace X] [Nonempty X]
    (μ : ℕ → Measure X) (a : ℕ → ℝ) (I : X → ℝ≥0∞) (F : X → ℝ),
      SatisfiesLDP μ a I → Continuous F → (∃ B : ℝ, ∀ x, |F x| ≤ B) →
      Tendsto (LogExpIntegral μ a F) atTop
        (𝓝 (⨆ x : X, (F x : EReal) - (I x : EReal)))

def mutationChangedDomain : Prop :=
  ∀ (μ : ℕ → Measure ℝ) (a : ℕ → ℝ) (I : ℝ → ℝ≥0∞) (F : ℝ → ℝ),
    SatisfiesLDP μ a I → IsGoodRateFunction I → Continuous F →
    (∃ B : ℝ, ∀ x, |F x| ≤ B) →
    Tendsto (LogExpIntegral μ a F) atTop
      (𝓝 (⨆ x : ℝ, (F x : EReal) - (I x : EReal)))

def mutationChangedBinderScope : Prop :=
  ∀ (X : Type u) [PseudoMetricSpace X] [CompleteSpace X]
    [SecondCountableTopology X] [MeasurableSpace X] [BorelSpace X] [Nonempty X]
    (μ : ℕ → Measure X) (a : ℕ → ℝ) (I : X → ℝ≥0∞),
      SatisfiesLDP μ a I → IsGoodRateFunction I →
      ∃ B : ℝ, ∀ F : X → ℝ, Continuous F → (∀ x, |F x| ≤ B) →
        Tendsto (LogExpIntegral μ a F) atTop
          (𝓝 (⨆ x : X, (F x : EReal) - (I x : EReal)))

def mutationAllowsZeroSpeed : Prop :=
  ∀ (X : Type u) [PseudoMetricSpace X] [CompleteSpace X]
    [SecondCountableTopology X] [MeasurableSpace X] [BorelSpace X] [Nonempty X]
    (μ : ℕ → Measure X) (a : ℕ → ℝ) (I : X → ℝ≥0∞) (F : X → ℝ),
      ((∀ n, IsProbabilityMeasure (μ n)) ∧ (∀ n, 0 ≤ a n) ∧
        Tendsto a atTop (𝓝 0)) → IsGoodRateFunction I → Continuous F →
      (∃ B : ℝ, ∀ x, |F x| ≤ B) →
      Tendsto (LogExpIntegral μ a F) atTop
        (𝓝 (⨆ x : X, (F x : EReal) - (I x : EReal)))

end Stage1Instances.THM_M_1061

set_option pp.explicit true in
#print Stage1Instances.THM_M_1061.VaradhanIntegralLemmaTarget
