import Mathlib.Analysis.Normed.Module.FiniteDimension
import Mathlib.Probability.Distributions.Gaussian.Real
import Mathlib.MeasureTheory.Measure.Prod

/-!
# THM-M-1244 anchor-audit probes

These declarations check only the repo-local interfaces used to compare the
canonical target with audited candidates.  They do not state or prove a
logarithmic Sobolev inequality.
-/

namespace Stage1Instances.THM_M_1244.AnchorAudit

open MeasureTheory ProbabilityTheory

abbrev Euclidean (n : Nat) := Fin n → ℝ

/-- The measure expression used by both the canonical target and the external candidate. -/
noncomputable def productGaussian (n : Nat) : Measure (Euclidean n) :=
  Measure.pi fun _ : Fin n ↦ gaussianReal 0 1

/-- The canonical target's energy density: operator norm for the product norm on `Fin n → ℝ`. -/
noncomputable def operatorNormEnergy {n : Nat} (f : Euclidean n → ℝ)
    (x : Euclidean n) : ℝ :=
  ‖fderiv ℝ f x‖ ^ 2

/-- The external candidate's energy density: a sum of squared coordinate derivatives. -/
noncomputable def coordinateSquareEnergy {n : Nat} (f : Euclidean n → ℝ)
    (x : Euclidean n) : ℝ :=
  ∑ i : Fin n, (fderiv ℝ f x (Pi.single i 1)) ^ 2

/-- Baseline control for the definitional comparison below. -/
example : (operatorNormEnergy : (Euclidean 2 → ℝ) → Euclidean 2 → ℝ) =
    operatorNormEnergy := rfl

-- Lean rejects a definitional identification of the two audited energy encodings.
#check_failure (rfl :
    (operatorNormEnergy : (Euclidean 2 → ℝ) → Euclidean 2 → ℝ) =
    coordinateSquareEnergy)

end Stage1Instances.THM_M_1244.AnchorAudit

#check MeasureTheory.Measure.pi
#check ProbabilityTheory.gaussianReal
#check MeasureTheory.MemLp.integrable_sq
