import Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Def

/-!
# THM-M-1088 obligation-tree interfaces

This module checks the exact child-to-root composition boundary selected by the frozen obligation
registry.  `UpperTailEngine` is deliberately an open central obligation, not an implementation of
Borell--TIS.  The theorem below only certifies that an implementation of that exact engine consumes
all canonical hypotheses and yields the frozen public target.
-/

noncomputable section

open MeasureTheory Set

namespace Stage1Instances.THM_M_1088

universe u v

-- Re-elaborated exact interfaces from `Statement.lean`; the registry binds both files by hash.
def IsSupremum {Ω T : Type*} (X : T → Ω → ℝ) (S : Ω → ℝ) : Prop :=
  ∀ ω, BddAbove (range fun t ↦ X t ω) ∧ S ω = sSup (range fun t ↦ X t ω)

def UpperTailBound {Ω : Type*} [MeasurableSpace Ω]
    (P : Measure Ω) (S : Ω → ℝ) (σ2 : ℝ) : Prop :=
  ∀ u : ℝ, 0 ≤ u →
    P {ω | u < S ω - ∫ x, S x ∂P} ≤ ENNReal.ofReal (Real.exp (-(u ^ 2) / (2 * σ2)))

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

namespace ObligationTree

/-- The open analytic engine after statement, normalization, finite approximation, concentration,
and limit-passage obligations have been composed. -/
def UpperTailEngine : Prop :=
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

/-- Checked composition certificate from the exact open engine to the exact canonical root. -/
theorem target_of_upperTailEngine
    (engine : @UpperTailEngine.{u, v}) : @BorellTISTarget.{u, v} := by
  intro Ω T _ _ _ P X S σ2 hGaussian hMeasurable hCentered hSup hInt hσ2 hVariance
  exact engine Ω T _ P X S σ2 hGaussian hMeasurable hCentered hSup hInt hσ2 hVariance

theorem upperTailEngine_iff_target :
    @UpperTailEngine.{u, v} ↔ @BorellTISTarget.{u, v} := by
  rfl

end ObligationTree
end Stage1Instances.THM_M_1088

#print axioms Stage1Instances.THM_M_1088.ObligationTree.target_of_upperTailEngine
