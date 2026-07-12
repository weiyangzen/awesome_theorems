import Mathlib.MeasureTheory.Measure.CharacteristicFunction.Basic

/-!
# THM-M-1018: exact Levy inversion statement

This module freezes and elaborates the interval-mass formulation selected at
intake. It contains no proof of the inversion formula.
-/

noncomputable section

open Filter MeasureTheory Set
open scoped ENNReal Topology

namespace Stage1Instances.THM_M_1018

/-- The Fourier kernel for the half-open interval `(a, b]`, extended at zero
by its removable value. The sign agrees with mathlib's `charFun` convention. -/
def levyIntervalKernel (a b t : Real) : Complex :=
  if t = 0 then (b - a : Real)
  else
    (Complex.exp (-Complex.I * (t : Complex) * (a : Complex)) -
        Complex.exp (-Complex.I * (t : Complex) * (b : Complex))) /
      (Complex.I * (t : Complex))

/-- Levy's inversion formula for a probability measure on `Real`, at two
ordered atom-free endpoints. -/
def LevyInversionTarget : Prop :=
  forall (mu : Measure Real) [IsProbabilityMeasure mu] (a b : Real),
    a < b ->
    mu {a} = 0 ->
    mu {b} = 0 ->
    Tendsto
      (fun T : Real =>
        ((1 : Complex) / (2 * Real.pi)) *
          integral (volume.restrict (Set.Icc (-T) T))
            (fun t : Real => levyIntervalKernel a b t * charFun mu t))
      atTop
      (nhds (((mu (Set.Ioc a b)).toReal : Real) : Complex))

/-- Binder-explicit encoding used to check that no hypothesis is hidden in
the canonical definition. -/
def ExpandedLevyInversionTarget : Prop :=
  forall (mu : Measure Real),
  forall [IsProbabilityMeasure mu],
  forall (a b : Real),
    a < b ->
    mu {a} = 0 ->
    mu {b} = 0 ->
    Tendsto
      (fun T : Real =>
        ((1 : Complex) / (2 * Real.pi)) *
          integral (volume.restrict (Set.Icc (-T) T))
            (fun t : Real => levyIntervalKernel a b t * charFun mu t))
      atTop
      (nhds (((mu (Set.Ioc a b)).toReal : Real) : Complex))

/-- Checked transport to the binder-explicit encoding. -/
theorem target_iff_expanded :
    LevyInversionTarget <-> ExpandedLevyInversionTarget := by
  rfl

-- Separately elaborated, deliberately changed mutation probes.
def mutationAllowsEndpointAtoms : Prop :=
  forall (mu : Measure Real) [IsProbabilityMeasure mu] (a b : Real),
    a < b ->
    Tendsto
      (fun T : Real =>
        ((1 : Complex) / (2 * Real.pi)) *
          integral (volume.restrict (Set.Icc (-T) T))
            (fun t : Real => levyIntervalKernel a b t * charFun mu t))
      atTop
      (nhds (((mu (Set.Ioc a b)).toReal : Real) : Complex))

def mutationOppositeTransformSign : Prop :=
  forall (mu : Measure Real) [IsProbabilityMeasure mu] (a b : Real),
    a < b -> mu {a} = 0 -> mu {b} = 0 ->
    Tendsto
      (fun T : Real =>
        ((1 : Complex) / (2 * Real.pi)) *
          integral (volume.restrict (Set.Icc (-T) T))
            (fun t : Real => levyIntervalKernel a b t * charFun mu (-t)))
      atTop
      (nhds (((mu (Set.Ioc a b)).toReal : Real) : Complex))

def mutationClosedInterval : Prop :=
  forall (mu : Measure Real) [IsProbabilityMeasure mu] (a b : Real),
    a < b -> mu {a} = 0 -> mu {b} = 0 ->
    Tendsto
      (fun T : Real =>
        ((1 : Complex) / (2 * Real.pi)) *
          integral (volume.restrict (Set.Icc (-T) T))
            (fun t : Real => levyIntervalKernel a b t * charFun mu t))
      atTop
      (nhds (((mu (Set.Icc a b)).toReal : Real) : Complex))

end Stage1Instances.THM_M_1018

set_option pp.explicit true in
#print Stage1Instances.THM_M_1018.LevyInversionTarget
