import Mathlib.MeasureTheory.Integral.Lebesgue.Basic
import Mathlib.Probability.Distributions.Gaussian.Real

/-!
# THM-M-1067 obligation composition interfaces

These declarations check only how the frozen open obligations compose. Their hypotheses are the
registered children; they are not proofs of Brownian local-time existence.
-/

noncomputable section

open MeasureTheory Set
open scoped ENNReal NNReal Topology

namespace Stage1Instances.THM_M_1067.ObligationTree

abbrev BrownianPath := {w : C(NNReal, Real) // w 0 = 0}

instance : MeasurableSpace BrownianPath := borel BrownianPath

def nonnegativeLebesgue : Measure NNReal := Measure.map Real.toNNReal volume

def IsWienerMeasure (W : Measure BrownianPath) : Prop :=
  IsProbabilityMeasure W ∧
    forall (n : Nat) (t : Fin n -> NNReal) (a : Fin n -> Real),
      exists v : NNReal,
        (v : Real) = ∑ i, ∑ j, a i * a j * min (t i : Real) (t j : Real) ∧
        Measure.map (fun w : BrownianPath => ∑ i, a i * w.1 (t i)) W =
          ProbabilityTheory.gaussianReal 0 v

def IsBrownianLocalTime (W : Measure BrownianPath)
    (L : BrownianPath -> NNReal -> Real -> NNReal) : Prop :=
  (forall t x, AEMeasurable (fun w => L w t x) W) ∧
    ∀ᵐ w ∂W, Continuous (Function.uncurry (L w)) ∧
      forall (t : NNReal) (f : Real -> ENNReal), Measurable f ->
        ∫⁻ s in Icc (0 : NNReal) t, f (w.1 s) ∂nonnegativeLebesgue =
          ∫⁻ x : Real, f x * (L w t x : ENNReal)

def BrownianLocalTimeTarget : Prop :=
  forall W : Measure BrownianPath, IsWienerMeasure W ->
    exists L : BrownianPath -> NNReal -> Real -> NNReal, IsBrownianLocalTime W L

def PointwiseMeasurable (W : Measure BrownianPath)
    (L : BrownianPath -> NNReal -> Real -> NNReal) : Prop :=
  forall t x, AEMeasurable (fun w => L w t x) W

def JointlyContinuousAE (W : Measure BrownianPath)
    (L : BrownianPath -> NNReal -> Real -> NNReal) : Prop :=
  ∀ᵐ w ∂W, Continuous (Function.uncurry (L w))

def OccupationIdentityAE (W : Measure BrownianPath)
    (L : BrownianPath -> NNReal -> Real -> NNReal) : Prop :=
  ∀ᵐ w ∂W, forall (t : NNReal) (f : Real -> ENNReal), Measurable f ->
    ∫⁻ s in Set.Icc (0 : NNReal) t, f (w.1 s) ∂nonnegativeLebesgue =
      ∫⁻ x : Real, f x * (L w t x : ENNReal)

theorem isBrownianLocalTime_of_components
    {W : Measure BrownianPath} {L : BrownianPath -> NNReal -> Real -> NNReal}
    (hMeas : PointwiseMeasurable W L)
    (hBoth : ∀ᵐ w ∂W, Continuous (Function.uncurry (L w)) ∧
      forall (t : NNReal) (f : Real -> ENNReal), Measurable f ->
        ∫⁻ s in Set.Icc (0 : NNReal) t, f (w.1 s) ∂nonnegativeLebesgue =
          ∫⁻ x : Real, f x * (L w t x : ENNReal)) :
    IsBrownianLocalTime W L := by
  exact ⟨hMeas, hBoth⟩

theorem brownianLocalTimeTarget_of_constructor
    (build : forall W : Measure BrownianPath, IsWienerMeasure W ->
      exists L : BrownianPath -> NNReal -> Real -> NNReal,
        PointwiseMeasurable W L ∧
        (∀ᵐ w ∂W, Continuous (Function.uncurry (L w)) ∧
          forall (t : NNReal) (f : Real -> ENNReal), Measurable f ->
            ∫⁻ s in Set.Icc (0 : NNReal) t, f (w.1 s) ∂nonnegativeLebesgue =
              ∫⁻ x : Real, f x * (L w t x : ENNReal))) :
    BrownianLocalTimeTarget := by
  intro W hW
  obtain ⟨L, hMeas, hBoth⟩ := build W hW
  exact ⟨L, isBrownianLocalTime_of_components hMeas hBoth⟩

end Stage1Instances.THM_M_1067.ObligationTree
