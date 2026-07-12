import Mathlib.MeasureTheory.Measure.CharacteristicFunction.Basic

/-!
# THM-M-1018 conditional obligation composition

This module checks the final binder-level composition for the frozen Levy
inversion target. The analytic inversion premise remains explicit; this file
does not prove it.
-/

noncomputable section

open Filter MeasureTheory Set
open scoped ENNReal Topology

namespace Stage1Instances.THM_M_1018.ObligationTree

def IntervalKernel (a b t : Real) : Complex :=
  if t = 0 then (b - a : Real)
  else
    (Complex.exp (-Complex.I * (t : Complex) * (a : Complex)) -
        Complex.exp (-Complex.I * (t : Complex) * (b : Complex))) /
      (Complex.I * (t : Complex))

def InversionFor (mu : Measure Real) (a b : Real) : Prop :=
  Tendsto
    (fun T : Real =>
      ((1 : Complex) / (2 * Real.pi)) *
        integral (volume.restrict (Set.Icc (-T) T))
          (fun t : Real =>
            IntervalKernel a b t * charFun mu t))
    atTop
    (nhds (((mu (Set.Ioc a b)).toReal : Real) : Complex))

/-- Exact child-to-root composition. The analytic inversion result is an
explicit premise for each probability measure and pair of atom-free ordered
endpoints. -/
theorem root_compose
    (analytic : forall (mu : Measure Real) [IsProbabilityMeasure mu] (a b : Real),
      a < b -> mu {a} = 0 -> mu {b} = 0 -> InversionFor mu a b) :
    forall (mu : Measure Real) [IsProbabilityMeasure mu] (a b : Real),
      a < b -> mu {a} = 0 -> mu {b} = 0 -> InversionFor mu a b := by
  intro mu _ a b hab ha hb
  exact analytic mu a b hab ha hb

#print axioms root_compose

end Stage1Instances.THM_M_1018.ObligationTree
