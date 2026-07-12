import Mathlib.Probability.Martingale.Convergence

/-!
# THM-M-1003: exact L^p martingale convergence statement

This module freezes the statement boundary only. It does not prove martingale
convergence.
-/

noncomputable section

open Filter MeasureTheory
open scoped ENNReal MeasureTheory NNReal Topology

universe u

namespace Stage1Instances.THM_M_1003

/-- The data in the classical discrete-time, real-valued `L^p` martingale
convergence theorem. The strict exponent regime is part of the data, while an
`L^1` bound is deliberately not an additional hypothesis. -/
structure LpBoundedMartingale (Omega : Type u) [MeasurableSpace Omega] : Type u where
  measure : Measure Omega
  finiteMeasure : IsFiniteMeasure measure
  filtration : Filtration Nat ‹MeasurableSpace Omega›
  process : Nat -> Omega -> Real
  martingale : Martingale process filtration measure
  exponent : ENNReal
  one_lt_exponent : 1 < exponent
  exponent_lt_top : exponent < infinity
  lpBounded : ∃ bound : NNReal,
    ∀ n : Nat, eLpNorm (process n) exponent measure ≤ bound

/-- Almost-sure and `L^p` convergence of a process to the same `L^p` random
variable. -/
def ConvergesAEAndInLp {Omega : Type u} [MeasurableSpace Omega]
    (D : LpBoundedMartingale Omega) (limit : Omega -> Real) : Prop :=
  MemLp limit D.exponent D.measure ∧
    (∀ᵐ omega ∂D.measure,
      Tendsto (fun n : Nat => D.process n omega) atTop (nhds (limit omega))) /\
    Tendsto
      (fun n : Nat =>
        eLpNorm (fun omega => D.process n omega - limit omega)
          D.exponent D.measure)
      atTop (nhds 0)

/-- Exact target: every real-valued discrete-time martingale bounded in `L^p`,
for `1 < p < infinity`, has a common almost-sure and `L^p` limit. -/
def LpMartingaleConvergenceTarget : Prop :=
  ∀ (Omega : Type u) [MeasurableSpace Omega]
    (D : LpBoundedMartingale Omega),
      ∃ limit : Omega -> Real, ConvergesAEAndInLp D limit

/-- Directly expanded form used to check the local statement packaging. -/
def ExpandedTarget : Prop :=
  ∀ (Omega : Type u) [MeasurableSpace Omega]
    (D : LpBoundedMartingale Omega),
      ∃ limit : Omega -> Real,
        MemLp limit D.exponent D.measure ∧
          (∀ᵐ omega ∂D.measure,
            Tendsto (fun n : Nat => D.process n omega) atTop (nhds (limit omega))) ∧
          Tendsto
            (fun n : Nat =>
              eLpNorm (fun omega => D.process n omega - limit omega)
                D.exponent D.measure)
            atTop (nhds 0)

/-- The package introduces no change to the expanded quantified claim. -/
theorem target_iff_expanded :
    LpMartingaleConvergenceTarget.{u} ↔ ExpandedTarget.{u} :=
  Iff.rfl

-- Separately elaborated structural mutations inspected by the statement check.
def mutationRemovedMartingale : Prop :=
  ∀ (Omega : Type u) [MeasurableSpace Omega]
    (D : LpBoundedMartingale Omega),
      ∃ limit : Omega -> Real,
        MemLp limit D.exponent D.measure

def mutationRemovedLpBound : Prop :=
  ∀ (Omega : Type u) [MeasurableSpace Omega]
    (measure : Measure Omega) (filtration : Filtration Nat ‹MeasurableSpace Omega›)
    (process : Nat -> Omega -> Real) (exponent : ENNReal),
      IsFiniteMeasure measure -> Martingale process filtration measure ->
      1 < exponent -> exponent < ∞ ->
      ∃ limit : Omega -> Real, MemLp limit exponent measure

def mutationIncludesEndpointOne : Prop :=
  ∀ (Omega : Type u) [MeasurableSpace Omega]
    (D : LpBoundedMartingale Omega),
      1 ≤ D.exponent -> ∃ limit : Omega -> Real, ConvergesAEAndInLp D limit

def mutationLpConvergenceOnly : Prop :=
  ∀ (Omega : Type u) [MeasurableSpace Omega]
    (D : LpBoundedMartingale Omega),
      ∃ limit : Omega -> Real,
        MemLp limit D.exponent D.measure ∧
          Tendsto
            (fun n : Nat =>
              eLpNorm (fun omega => D.process n omega - limit omega)
                D.exponent D.measure)
            atTop (nhds 0)

/-- The lower endpoint is genuinely excluded by the frozen data. -/
theorem exponent_ne_one {Omega : Type u} [MeasurableSpace Omega]
    (D : LpBoundedMartingale Omega) : D.exponent ≠ 1 :=
  ne_of_gt D.one_lt_exponent

/-- The infinite exponent endpoint is genuinely excluded by the frozen data. -/
theorem exponent_ne_top {Omega : Type u} [MeasurableSpace Omega]
    (D : LpBoundedMartingale Omega) : D.exponent ≠ infinity :=
  ne_of_lt D.exponent_lt_top

end Stage1Instances.THM_M_1003

set_option pp.explicit true in
#print Stage1Instances.THM_M_1003.LpMartingaleConvergenceTarget

set_option pp.explicit true in
#print Stage1Instances.THM_M_1003.mutationRemovedMartingale

set_option pp.explicit true in
#print Stage1Instances.THM_M_1003.mutationRemovedLpBound

set_option pp.explicit true in
#print Stage1Instances.THM_M_1003.mutationIncludesEndpointOne

set_option pp.explicit true in
#print Stage1Instances.THM_M_1003.mutationLpConvergenceOnly
