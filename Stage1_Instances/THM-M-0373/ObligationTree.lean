import Mathlib.Analysis.Complex.UnitDisc.Basic
import Mathlib.Analysis.Analytic.Basic
import Mathlib.Topology.MetricSpace.Bounded

/-!
# THM-M-0373 conditional obligation composition

This file checks the final child-to-parent interface for the frozen corona
architecture.  `BoundedAnalyticBezout` is deliberately a premise: no corona
proof or child closure is claimed here.
-/

namespace Stage1Instances.THM_M_0373.ObligationTree

open Metric Set

def unitDisc : Set ℂ := ball 0 1

def InHInfinity (f : ℂ → ℂ) : Prop :=
  AnalyticOnNhd ℂ f unitDisc ∧ Bornology.IsBounded (f '' unitDisc)

def CoronaTarget : Prop :=
  ∀ (ι : Type) [Fintype ι] [Nonempty ι] (f : ι → ℂ → ℂ) (δ : ℝ),
    (∀ i, InHInfinity (f i)) → 0 < δ →
    (∀ z ∈ unitDisc, δ ≤ ∑ i, ‖f i z‖) →
    ∃ g : ι → ℂ → ℂ, (∀ i, InHInfinity (g i)) ∧
      ∀ z ∈ unitDisc, ∑ i, f i z * g i z = 1

/-- The final mathematical child has the exact expanded target type. -/
def BoundedAnalyticBezout : Prop := CoronaTarget

/-- Definitional child-to-root composition only; the premise remains open. -/
theorem root_compose (h : BoundedAnalyticBezout) : CoronaTarget := by
  exact h

#check root_compose
#print axioms root_compose

end Stage1Instances.THM_M_0373.ObligationTree
