import Mathlib.Analysis.SpecialFunctions.Log.ENNRealLog
import Mathlib.MeasureTheory.Integral.IntervalIntegral.Basic
import Mathlib.Probability.Distributions.Gaussian.Real

/-! Checked composition interfaces for the frozen THM-M-1060 architecture. -/

noncomputable section

open Filter MeasureTheory Set Topology
open scoped ENNReal NNReal Topology

namespace Stage1Instances.THM_M_1060.ObligationTree

abbrev BasedPath := {f : C(Icc (0 : Real) 1, Real) // f ⟨0, by norm_num⟩ = 0}

instance : MeasurableSpace BasedPath := borel BasedPath

def scale (c : Real) : BasedPath → BasedPath := fun f ↦
  ⟨c • f.1, by simp only [ContinuousMap.coe_smul, Pi.smul_apply, smul_eq_mul, f.2, mul_zero]⟩

def IsWienerMeasure (W : Measure BasedPath) : Prop :=
  IsProbabilityMeasure W ∧
    ∀ (n : Nat) (t : Fin n → Icc (0 : Real) 1) (a : Fin n → Real),
      ∃ v : NNReal,
        (v : Real) = ∑ i, ∑ j, a i * a j * min (t i : Real) (t j : Real) ∧
        Measure.map (fun f : BasedPath ↦ ∑ i, a i * f.1 (t i)) W =
          ProbabilityTheory.gaussianReal 0 v

def cameronMartinRate (f : BasedPath) : EReal :=
  sInf {r : EReal | ∃ g : Real → Real,
    IntegrableOn g (Icc (0 : Real) 1) ∧
    IntegrableOn (fun t ↦ g t ^ 2) (Icc (0 : Real) 1) ∧
    (∀ t : Icc (0 : Real) 1, f.1 t = ∫ x in (0 : Real)..t, g x) ∧
    r = ((∫ x in (0 : Real)..1, g x ^ 2) / 2 : Real)}

def law (W : Measure BasedPath) (ε : Real) : Measure BasedPath :=
  Measure.map (scale (Real.sqrt ε)) W

def OpenLower (W : Measure BasedPath) : Prop :=
  ∀ G : Set BasedPath, IsOpen G →
    -(sInf (cameronMartinRate '' G)) ≤
      liminf (fun ε : Real ↦ (ε : EReal) * ENNReal.log (law W ε G)) (nhdsWithin 0 (Ioi 0))

def ClosedUpper (W : Measure BasedPath) : Prop :=
  ∀ F : Set BasedPath, IsClosed F →
    limsup (fun ε : Real ↦ (ε : EReal) * ENNReal.log (law W ε F)) (nhdsWithin 0 (Ioi 0)) ≤
      -(sInf (cameronMartinRate '' F))

def GoodRate : Prop := ∀ a : Real, IsCompact {f | cameronMartinRate f ≤ a}

def SmallNoiseLDP (W : Measure BasedPath) : Prop := OpenLower W ∧ ClosedUpper W ∧ GoodRate

def SchilderTarget : Prop := ∀ W : Measure BasedPath, IsWienerMeasure W → SmallNoiseLDP W

/-- Exact conjunction composition. Its hypotheses are open obligations, not proof bodies. -/
theorem smallNoiseLDP_of_bounds_and_good (W : Measure BasedPath)
    (lower : OpenLower W) (upper : ClosedUpper W) (good : GoodRate) : SmallNoiseLDP W := by
  exact ⟨lower, upper, good⟩

/-- Root composition consumes all three registered terminal packages for each Wiener law. -/
theorem schilderTarget_of_components
    (lower : ∀ W, IsWienerMeasure W → OpenLower W)
    (upper : ∀ W, IsWienerMeasure W → ClosedUpper W)
    (good : GoodRate) : SchilderTarget := by
  intro W hW
  exact smallNoiseLDP_of_bounds_and_good W (lower W hW) (upper W hW) good

#check smallNoiseLDP_of_bounds_and_good
#check schilderTarget_of_components

end Stage1Instances.THM_M_1060.ObligationTree
