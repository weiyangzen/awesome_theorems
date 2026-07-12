import Mathlib.Probability.Distributions.Gaussian.Real
import Mathlib.Probability.Martingale.Basic

/-!
# THM-M-1029: exact Levy martingale-characterization statement

This module freezes the statement boundary only. It does not prove Levy's
characterization.
-/

noncomputable section

open MeasureTheory ProbabilityTheory
open scoped ENNReal NNReal MeasureTheory ProbabilityTheory

namespace Stage1Instances.THM_M_1029

universe u

/-- Nonnegative real time and real-valued processes. -/
abbrev Time := ℝ≥0
abbrev RealProcess (Ω : Type u) := Time → Ω → ℝ

/-- The compensated square in Levy's characterization. -/
def QuadraticCompensated {Ω : Type u} (X : RealProcess Ω) : RealProcess Ω :=
  fun t ω => X t ω ^ 2 - (t : ℝ)

/-- Standard Brownian motion relative to a specified filtration: continuous
paths, zero start, and every future increment is independent of the past and
has the centered Gaussian law whose variance is elapsed time. -/
def IsBrownianMotionRelative {Ω : Type u} [MeasurableSpace Ω]
    (X : RealProcess Ω) (P : Measure Ω)
    (ℱ : Filtration Time (inferInstance : MeasurableSpace Ω)) : Prop :=
  (∀ ω : Ω, Continuous fun t : Time => X t ω) ∧
    X 0 =ᵐ[P] 0 ∧
      ∀ ⦃s t : Time⦄, s ≤ t →
        Indep (ℱ s)
            (MeasurableSpace.comap (fun ω => X t ω - X s ω) (borel ℝ)) P ∧
          HasLaw (fun ω => X t ω - X s ω)
            (gaussianReal 0 (t - s)) P

/-- The exact selected form of Levy's martingale characterization. -/
def LevyMartingaleCharacterizationTarget : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω]
    (P : Measure Ω) [IsProbabilityMeasure P]
    (ℱ : Filtration Time (inferInstance : MeasurableSpace Ω))
    (X : RealProcess Ω),
      (∀ ω : Ω, Continuous fun t : Time => X t ω) →
      X 0 =ᵐ[P] 0 →
      Martingale X ℱ P →
      Martingale (QuadraticCompensated X) ℱ P →
      IsBrownianMotionRelative X P ℱ

/-- Direct expansion of the selected target, used as a checked transport. -/
def ExpandedSourceShape : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω]
    (P : Measure Ω) [IsProbabilityMeasure P]
    (ℱ : Filtration Time (inferInstance : MeasurableSpace Ω))
    (X : RealProcess Ω),
      (∀ ω : Ω, Continuous fun t : Time => X t ω) →
      X 0 =ᵐ[P] 0 →
      Martingale X ℱ P →
      Martingale (fun t ω => X t ω ^ 2 - (t : ℝ)) ℱ P →
      (∀ ω : Ω, Continuous fun t : Time => X t ω) ∧
        X 0 =ᵐ[P] 0 ∧
          ∀ ⦃s t : Time⦄, s ≤ t →
            Indep (ℱ s)
                (MeasurableSpace.comap (fun ω => X t ω - X s ω) (borel ℝ)) P ∧
              HasLaw (fun ω => X t ω - X s ω)
                (gaussianReal 0 (t - s)) P

theorem target_iff_expandedSourceShape :
    LevyMartingaleCharacterizationTarget.{u} ↔ ExpandedSourceShape.{u} := by
  rfl

-- Separately elaborated, deliberately non-equivalent structural mutations.
def mutationRemovedQuadraticMartingale : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω] (P : Measure Ω) [IsProbabilityMeasure P]
    (ℱ : Filtration Time (inferInstance : MeasurableSpace Ω)) (X : RealProcess Ω),
    (∀ ω, Continuous fun t => X t ω) → X 0 =ᵐ[P] 0 → Martingale X ℱ P →
      IsBrownianMotionRelative X P ℱ

def mutationChangedDomainToNaturalTime : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω] (P : Measure Ω),
    ∀ X : Nat → Ω → ℝ, X 0 =ᵐ[P] 0 → True

def mutationChangedBinderScope : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω] (P : Measure Ω) [IsProbabilityMeasure P]
    (X : RealProcess Ω),
    ∃ ℱ : Filtration Time (inferInstance : MeasurableSpace Ω),
      Martingale X ℱ P → IsBrownianMotionRelative X P ℱ

def mutationExcludedZeroElapsedIncrement : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω] (P : Measure Ω)
    (ℱ : Filtration Time (inferInstance : MeasurableSpace Ω)) (X : RealProcess Ω),
    ∀ ⦃s t : Time⦄, s < t →
      HasLaw (fun ω => X t ω - X s ω) (gaussianReal 0 (t - s)) P

/-- At the boundary `s = t`, the target specifies the zero-variance Gaussian. -/
theorem zeroElapsedVariance (t : Time) : t - t = 0 := by simp

end Stage1Instances.THM_M_1029

set_option pp.explicit true in
#print Stage1Instances.THM_M_1029.LevyMartingaleCharacterizationTarget
