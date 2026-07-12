import Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Def

/-!
# THM-M-1088: Borell--TIS statement

This module freezes the one-sided concentration form for a nonempty countable real Gaussian
process.  The measurable real random variable `S` is an explicitly supplied representative of
the pointwise supremum.  Integrability of `S` and a strictly positive finite variance proxy are
stated explicitly; the zero-variance extension is not silently obtained from division in `ℝ`.

No proof of Borell--TIS is supplied in this statement module.
-/

noncomputable section

open MeasureTheory Set
open scoped ENNReal

namespace Stage1Instances.THM_M_1088

universe u v

/-- `S` is the pointwise supremum of the process.  Boundedness is explicit because `sSup` on
`ℝ` otherwise uses the conditionally-complete-lattice default outside its mathematical domain. -/
def IsSupremum {Ω T : Type*} (X : T → Ω → ℝ) (S : Ω → ℝ) : Prop :=
  ∀ ω, BddAbove (range fun t ↦ X t ω) ∧ S ω = sSup (range fun t ↦ X t ω)

/-- The one-sided Borell--TIS upper-tail conclusion with variance parameter `σ2`. -/
def UpperTailBound {Ω : Type*} [MeasurableSpace Ω]
    (P : Measure Ω) (S : Ω → ℝ) (σ2 : ℝ) : Prop :=
  ∀ u : ℝ, 0 ≤ u →
    P {ω | u < S ω - ∫ x, S x ∂P} ≤ ENNReal.ofReal (Real.exp (-(u ^ 2) / (2 * σ2)))

/-- Canonical countable-index Borell--TIS target.

The positive equation for `σ2` both fixes the normalization and excludes the degenerate
zero-variance case.  Countability is the selected separability convention: it makes the supremum
measurable from the coordinate measurability supplied separately below. -/
def BorellTISTarget : Prop :=
  ∀ (Ω T : Type*) (_ : MeasurableSpace Ω) [Countable T] [Nonempty T]
      (P : Measure Ω) (X : T → Ω → ℝ) (S : Ω → ℝ) (σ2 : ℝ),
    ProbabilityTheory.IsGaussianProcess X P →
    (∀ t, Measurable (X t)) →
    (∀ t, ∫ ω, X t ω ∂P = 0) →
    IsSupremum X S →
    Integrable S P →
    0 < σ2 →
    σ2 = sSup (range fun t ↦ ProbabilityTheory.variance (X t) P) →
    UpperTailBound P S σ2

/-- Directly expanded source shape, used to check that the named predicates hide no additional
mathematical strength. -/
def ExpandedSourceShape : Prop :=
  ∀ (Ω T : Type*) (_ : MeasurableSpace Ω) [Countable T] [Nonempty T]
      (P : Measure Ω) (X : T → Ω → ℝ) (S : Ω → ℝ) (σ2 : ℝ),
    ProbabilityTheory.IsGaussianProcess X P →
    (∀ t, Measurable (X t)) →
    (∀ t, ∫ ω, X t ω ∂P = 0) →
    (∀ ω, BddAbove (range fun t ↦ X t ω) ∧ S ω = sSup (range fun t ↦ X t ω)) →
    Integrable S P →
    0 < σ2 →
    σ2 = sSup (range fun t ↦ ProbabilityTheory.variance (X t) P) →
    ∀ u : ℝ, 0 ≤ u →
      P {ω | u < S ω - ∫ x, S x ∂P} ≤
        ENNReal.ofReal (Real.exp (-(u ^ 2) / (2 * σ2)))

theorem target_iff_expandedSourceShape :
    @BorellTISTarget.{u, v} ↔ @ExpandedSourceShape.{u, v} := by
  simp only [BorellTISTarget, ExpandedSourceShape, IsSupremum, UpperTailBound]

-- Deliberately non-equivalent mutations retained for statement-boundary review.
def mutationRemovedGaussianHypothesis : Prop :=
  ∀ (Ω T : Type*) (_ : MeasurableSpace Ω) [Countable T] [Nonempty T]
      (P : Measure Ω) (X : T → Ω → ℝ) (S : Ω → ℝ) (σ2 : ℝ),
    (∀ t, Measurable (X t)) → IsSupremum X S → Integrable S P → 0 < σ2 →
    UpperTailBound P S σ2

def mutationFiniteDomain : Prop :=
  ∀ (Ω T : Type*) (_ : MeasurableSpace Ω) [Fintype T] [Nonempty T]
      (P : Measure Ω) (X : T → Ω → ℝ) (S : Ω → ℝ) (σ2 : ℝ),
    ProbabilityTheory.IsGaussianProcess X P → IsSupremum X S → Integrable S P → 0 < σ2 →
    UpperTailBound P S σ2

def mutationPositiveTailOnly : Prop :=
  ∀ (Ω T : Type*) (_ : MeasurableSpace Ω) [Countable T] [Nonempty T]
      (P : Measure Ω) (X : T → Ω → ℝ) (S : Ω → ℝ) (σ2 : ℝ),
    ProbabilityTheory.IsGaussianProcess X P → IsSupremum X S → Integrable S P → 0 < σ2 →
    ∀ u : ℝ, 0 < u →
      P {ω | u < S ω - ∫ x, S x ∂P} ≤
        ENNReal.ofReal (Real.exp (-(u ^ 2) / (2 * σ2)))

def mutationAllowsZeroVariance : Prop :=
  ∀ (Ω T : Type*) (_ : MeasurableSpace Ω) [Countable T] [Nonempty T]
      (P : Measure Ω) (X : T → Ω → ℝ) (S : Ω → ℝ) (σ2 : ℝ),
    ProbabilityTheory.IsGaussianProcess X P → IsSupremum X S → Integrable S P → 0 ≤ σ2 →
    UpperTailBound P S σ2

end Stage1Instances.THM_M_1088

set_option pp.explicit true in
#print Stage1Instances.THM_M_1088.BorellTISTarget
