import Mathlib.Analysis.SpecialFunctions.Log.ENNRealLog
import Mathlib.MeasureTheory.Integral.IntervalIntegral.Basic
import Mathlib.Probability.Distributions.Gaussian.Real

/-!
# THM-M-1060: exact Schilder theorem statement

This module freezes Schilder's theorem on `[0, 1]`.  It states the full open-set lower bound,
closed-set upper bound, and goodness of the Cameron--Martin rate function.  No proof of Schilder's
theorem is supplied here.
-/

noncomputable section

open Filter MeasureTheory Set Topology
open scoped ENNReal NNReal Topology

namespace Stage1Instances.THM_M_1060

/-- Continuous real paths on `[0, 1]` which start at zero. -/
abbrev BasedPath := {f : C(Icc (0 : ℝ) 1, ℝ) // f ⟨0, by norm_num⟩ = 0}

instance : MeasurableSpace BasedPath := borel BasedPath

/-- Multiplication of a based path by a scalar. -/
def scale (c : ℝ) : BasedPath → BasedPath := fun f ↦
  ⟨c • f.1, by simp only [ContinuousMap.coe_smul, Pi.smul_apply, smul_eq_mul, f.2, mul_zero]⟩

/-- The finite-dimensional-distribution characterization of Wiener measure on based paths. -/
def IsWienerMeasure (W : Measure BasedPath) : Prop :=
  IsProbabilityMeasure W ∧
    ∀ (n : ℕ) (t : Fin n → Icc (0 : ℝ) 1) (a : Fin n → ℝ),
      ∃ v : ℝ≥0,
        (v : ℝ) = ∑ i, ∑ j, a i * a j * min (t i : ℝ) (t j : ℝ) ∧
        Measure.map (fun f : BasedPath ↦ ∑ i, a i * f.1 (t i)) W =
          ProbabilityTheory.gaussianReal 0 v

/-- Cameron--Martin energy.  The witness `g` is the a.e. derivative, encoded by the integral
representation; outside the Cameron--Martin space the energy is `∞`. -/
def cameronMartinRate (f : BasedPath) : EReal :=
  sInf {r : EReal | ∃ g : ℝ → ℝ,
    IntegrableOn g (Icc (0 : ℝ) 1) ∧
    IntegrableOn (fun t ↦ g t ^ 2) (Icc (0 : ℝ) 1) ∧
    (∀ t : Icc (0 : ℝ) 1, f.1 t = ∫ x in (0 : ℝ)..t, g x) ∧
    r = ((∫ x in (0 : ℝ)..1, g x ^ 2) / 2 : ℝ)}

/-- The large-deviation principle at small-noise scale `ε`, using the convention
`ε log με(A)`. -/
def SmallNoiseLDP (law : ℝ → Measure BasedPath) (rate : BasedPath → EReal) : Prop :=
  (∀ G : Set BasedPath, IsOpen G →
    -(sInf (rate '' G)) ≤
      liminf (fun ε : ℝ ↦ (ε : EReal) * ENNReal.log (law ε G)) (nhdsWithin 0 (Ioi 0))) ∧
  (∀ F : Set BasedPath, IsClosed F →
    limsup (fun ε : ℝ ↦ (ε : EReal) * ENNReal.log (law ε F)) (nhdsWithin 0 (Ioi 0)) ≤
      -(sInf (rate '' F))) ∧
  ∀ a : ℝ, IsCompact {f | rate f ≤ a}

/-- Schilder's theorem for standard Wiener measure on `C₀([0,1], ℝ)`. -/
def SchilderTarget : Prop :=
  ∀ W : Measure BasedPath, IsWienerMeasure W →
    SmallNoiseLDP
      (fun ε ↦ Measure.map (scale (Real.sqrt ε)) W)
      cameronMartinRate

/-- Direct expansion used to check that no strength is hidden in the theorem name. -/
def ExpandedSourceShape : Prop :=
  ∀ W : Measure BasedPath, IsWienerMeasure W →
    (∀ G : Set BasedPath, IsOpen G →
      -(sInf (cameronMartinRate '' G)) ≤
        liminf (fun ε : ℝ ↦ (ε : EReal) *
          ENNReal.log (Measure.map (scale (Real.sqrt ε)) W G)) (nhdsWithin 0 (Ioi 0))) ∧
    (∀ F : Set BasedPath, IsClosed F →
      limsup (fun ε : ℝ ↦ (ε : EReal) *
        ENNReal.log (Measure.map (scale (Real.sqrt ε)) W F)) (nhdsWithin 0 (Ioi 0)) ≤
          -(sInf (cameronMartinRate '' F))) ∧
    ∀ a : ℝ, IsCompact {f | cameronMartinRate f ≤ a}

theorem target_iff_expandedSourceShape : SchilderTarget ↔ ExpandedSourceShape := by
  rfl

-- Deliberately non-equivalent mutations, retained as statement-boundary checks.
def mutationOnlyClosedUpperBound : Prop :=
  ∀ W : Measure BasedPath, IsWienerMeasure W →
    ∀ F : Set BasedPath, IsClosed F →
      limsup (fun ε : ℝ ↦ (ε : EReal) *
        ENNReal.log (Measure.map (scale (Real.sqrt ε)) W F)) (nhdsWithin 0 (Ioi 0)) ≤
          -(sInf (cameronMartinRate '' F))

def mutationFiniteDimensionalDomain : Prop :=
  ∀ W : Measure ℝ, IsProbabilityMeasure W → True

def mutationAssumedLDP : Prop :=
  ∀ W : Measure BasedPath, SmallNoiseLDP (fun _ ↦ W) cameronMartinRate →
    SmallNoiseLDP (fun _ ↦ W) cameronMartinRate

end Stage1Instances.THM_M_1060

set_option pp.explicit true in
#print Stage1Instances.THM_M_1060.SchilderTarget
