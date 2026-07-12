import Mathlib.MeasureTheory.Measure.ProbabilityMeasure
import Mathlib.MeasureTheory.Integral.Bochner.Basic

/-!
# THM-M-1184: exact compact Kantorovich-duality statement

This module freezes the compact-metric, continuous real-cost statement selected
at intake. It states the target only and contains no proof of duality.
-/

noncomputable section

open MeasureTheory Set

namespace Stage1Instances.THM_M_1184

universe u v

variable {X : Type u} {Y : Type v}
  [MetricSpace X] [MeasurableSpace X] [BorelSpace X] [CompactSpace X]
  [MetricSpace Y] [MeasurableSpace Y] [BorelSpace Y] [CompactSpace Y]

/-- A probability coupling whose coordinate push-forwards are the prescribed
marginals. -/
structure Coupling (mu : ProbabilityMeasure X) (nu : ProbabilityMeasure Y) where
  plan : ProbabilityMeasure (X × Y)
  fst_marginal : Measure.map Prod.fst (plan : Measure (X × Y)) = (mu : Measure X)
  snd_marginal : Measure.map Prod.snd (plan : Measure (X × Y)) = (nu : Measure Y)

/-- A pair of signed continuous potentials satisfying the Kantorovich
pointwise constraint. -/
structure DualPair (c : X × Y → Real) where
  phi : X → Real
  psi : Y → Real
  phi_continuous : Continuous phi
  psi_continuous : Continuous psi
  feasible : ∀ x y, phi x + psi y ≤ c (x, y)

/-- Cost of one coupling. Compactness and continuity make this integral finite. -/
def PrimalValue {mu : ProbabilityMeasure X} {nu : ProbabilityMeasure Y}
    (c : X × Y → Real) (gamma : Coupling mu nu) : Real :=
  ∫ z, c z ∂(gamma.plan : Measure (X × Y))

/-- Objective of one feasible signed continuous potential pair. -/
def DualValue (mu : ProbabilityMeasure X) (nu : ProbabilityMeasure Y)
    (c : X × Y → Real) (p : DualPair c) : Real :=
  (∫ x, p.phi x ∂(mu : Measure X)) + ∫ y, p.psi y ∂(nu : Measure Y)

/-- The exact compact/continuous signed-real Kantorovich-duality target.

`sInf` and `sSup` express the mathematical infimum and supremum directly. The
indexed sets are nonempty: product couplings and constant feasible potentials
will be established in the proof architecture, rather than assumed here. -/
def KantorovichDualityTarget : Prop :=
  ∀ (X : Type u) (Y : Type v)
    [MetricSpace X] [MeasurableSpace X] [BorelSpace X] [CompactSpace X]
    [MetricSpace Y] [MeasurableSpace Y] [BorelSpace Y] [CompactSpace Y]
    (mu : ProbabilityMeasure X) (nu : ProbabilityMeasure Y)
    (c : X × Y → Real),
    Continuous c →
      sInf (range (PrimalValue (mu := mu) (nu := nu) c)) =
        sSup (range (DualValue mu nu c))

-- Structural mutations: these elaborate independently and are compared by the
-- statement validator; none is accepted as the target.
def mutationRemovedContinuity : Prop :=
  ∀ (X : Type u) (Y : Type v)
    [MetricSpace X] [MeasurableSpace X] [BorelSpace X] [CompactSpace X]
    [MetricSpace Y] [MeasurableSpace Y] [BorelSpace Y] [CompactSpace Y]
    (mu : ProbabilityMeasure X) (nu : ProbabilityMeasure Y)
    (c : X × Y → Real),
      sInf (range (PrimalValue (mu := mu) (nu := nu) c)) =
        sSup (range (DualValue mu nu c))

def mutationENNRealCost : Prop :=
  ∀ (X : Type u) (Y : Type v)
    [MetricSpace X] [MeasurableSpace X] [BorelSpace X] [CompactSpace X]
    [MetricSpace Y] [MeasurableSpace Y] [BorelSpace Y] [CompactSpace Y]
    (_mu : ProbabilityMeasure X) (_nu : ProbabilityMeasure Y)
    (c : X × Y → ENNReal), Continuous c → Nonempty (DualPair (fun z => (c z).toReal))

def mutationNonnegativePotentials : Prop :=
  ∀ (X : Type u) (Y : Type v)
    [MetricSpace X] [MeasurableSpace X] [BorelSpace X] [CompactSpace X]
    [MetricSpace Y] [MeasurableSpace Y] [BorelSpace Y] [CompactSpace Y]
    (_mu : ProbabilityMeasure X) (_nu : ProbabilityMeasure Y)
    (c : X × Y → Real), Continuous c →
      ∃ phi : X → NNReal, ∃ psi : Y → NNReal,
        ∀ x y, (phi x : Real) + (psi y : Real) ≤ c (x, y)

def mutationEqualityToWeakDuality : Prop :=
  ∀ (X : Type u) (Y : Type v)
    [MetricSpace X] [MeasurableSpace X] [BorelSpace X] [CompactSpace X]
    [MetricSpace Y] [MeasurableSpace Y] [BorelSpace Y] [CompactSpace Y]
    (mu : ProbabilityMeasure X) (nu : ProbabilityMeasure Y)
    (c : X × Y → Real), Continuous c →
      sSup (range (DualValue mu nu c)) ≤
        sInf (range (PrimalValue (mu := mu) (nu := nu) c))

/-- The zero pair is feasible for zero cost, including signed potentials. -/
def zeroDualPair : DualPair (X := X) (Y := Y) (fun _ => 0) where
  phi := fun _ => 0
  psi := fun _ => 0
  phi_continuous := continuous_const
  psi_continuous := continuous_const
  feasible := by simp

omit [MeasurableSpace X] [BorelSpace X] [CompactSpace X]
    [MeasurableSpace Y] [BorelSpace Y] [CompactSpace Y] in
theorem zero_cost_dual_nonempty :
    Nonempty (DualPair (X := X) (Y := Y) (fun _ => 0)) :=
  ⟨zeroDualPair⟩

end Stage1Instances.THM_M_1184

set_option pp.explicit true in
#print Stage1Instances.THM_M_1184.KantorovichDualityTarget
