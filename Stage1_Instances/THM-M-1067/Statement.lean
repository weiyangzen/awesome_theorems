import Mathlib.MeasureTheory.Integral.Lebesgue.Basic
import Mathlib.Probability.Distributions.Gaussian.Real

/-!
# THM-M-1067: exact Brownian local-time statement

This module freezes the existence of a jointly continuous local-time field for standard
one-dimensional Brownian motion, normalized by the occupation-density formula. It supplies no
proof of that existence theorem.
-/

noncomputable section

open MeasureTheory Set
open scoped ENNReal NNReal Topology

namespace Stage1Instances.THM_M_1067

/-- Continuous real paths on nonnegative time which start at zero. -/
abbrev BrownianPath := {w : C(ℝ≥0, ℝ) // w 0 = 0}

instance : MeasurableSpace BrownianPath := borel BrownianPath

/-- Lebesgue measure transported to nonnegative time. -/
def nonnegativeLebesgue : Measure ℝ≥0 := Measure.map Real.toNNReal volume

/-- The finite-dimensional-distribution characterization of standard Wiener measure on the
continuous based path space. -/
def IsWienerMeasure (W : Measure BrownianPath) : Prop :=
  IsProbabilityMeasure W ∧
    ∀ (n : ℕ) (t : Fin n → ℝ≥0) (a : Fin n → ℝ),
      ∃ v : ℝ≥0,
        (v : ℝ) = ∑ i, ∑ j, a i * a j * min (t i : ℝ) (t j : ℝ) ∧
        Measure.map (fun w : BrownianPath ↦ ∑ i, a i * w.1 (t i)) W =
          ProbabilityTheory.gaussianReal 0 v

/-- A field is a Brownian local time when its point evaluations are measurable and, outside one
null set, it is jointly continuous and satisfies the occupation-density identity simultaneously
for every time and every nonnegative Borel test function. -/
def IsBrownianLocalTime (W : Measure BrownianPath)
    (L : BrownianPath → ℝ≥0 → ℝ → ℝ≥0) : Prop :=
  (∀ t x, AEMeasurable (fun w ↦ L w t x) W) ∧
    ∀ᵐ w ∂W, Continuous (Function.uncurry (L w)) ∧
      ∀ (t : ℝ≥0) (f : ℝ → ℝ≥0∞), Measurable f →
        ∫⁻ s in Icc (0 : ℝ≥0) t, f (w.1 s) ∂nonnegativeLebesgue =
          ∫⁻ x : ℝ, f x * (L w t x : ℝ≥0∞)

/-- Every standard one-dimensional Wiener measure admits a jointly continuous local-time field,
with the occupation-density normalization (and hence no Tanaka factor-of-two ambiguity). -/
def BrownianLocalTimeTarget : Prop :=
  ∀ W : Measure BrownianPath, IsWienerMeasure W →
    ∃ L : BrownianPath → ℝ≥0 → ℝ → ℝ≥0, IsBrownianLocalTime W L

/-- Direct expansion used to check that the named target hides no extra strength. -/
def ExpandedSourceShape : Prop :=
  ∀ W : Measure BrownianPath, IsWienerMeasure W →
    ∃ L : BrownianPath → ℝ≥0 → ℝ → ℝ≥0,
      (∀ t x, AEMeasurable (fun w ↦ L w t x) W) ∧
        ∀ᵐ w ∂W, Continuous (Function.uncurry (L w)) ∧
          ∀ (t : ℝ≥0) (f : ℝ → ℝ≥0∞), Measurable f →
            ∫⁻ s in Icc (0 : ℝ≥0) t, f (w.1 s) ∂nonnegativeLebesgue =
              ∫⁻ x : ℝ, f x * (L w t x : ℝ≥0∞)

theorem target_iff_expandedSourceShape : BrownianLocalTimeTarget ↔ ExpandedSourceShape := by
  rfl

-- Deliberately weaker or circular mutations, retained as statement-boundary checks.
def mutationFixedLevel : Prop :=
  ∀ W : Measure BrownianPath, IsWienerMeasure W →
    ∃ L : BrownianPath → ℝ≥0 → ℝ≥0, ∀ t, AEMeasurable (fun w ↦ L w t) W

def mutationFixedTestFunction : Prop :=
  ∀ W : Measure BrownianPath, IsWienerMeasure W →
    ∀ f : ℝ → ℝ≥0∞, Measurable f →
      ∃ L : BrownianPath → ℝ≥0 → ℝ → ℝ≥0,
        ∀ᵐ w ∂W, ∀ t : ℝ≥0,
          ∫⁻ s in Icc (0 : ℝ≥0) t, f (w.1 s) ∂nonnegativeLebesgue =
            ∫⁻ x : ℝ, f x * (L w t x : ℝ≥0∞)

def mutationAssumedLocalTime : Prop :=
  ∀ W : Measure BrownianPath, IsWienerMeasure W →
    ∀ L : BrownianPath → ℝ≥0 → ℝ → ℝ≥0,
      IsBrownianLocalTime W L → IsBrownianLocalTime W L

end Stage1Instances.THM_M_1067

set_option pp.explicit true in
#print Stage1Instances.THM_M_1067.BrownianLocalTimeTarget
