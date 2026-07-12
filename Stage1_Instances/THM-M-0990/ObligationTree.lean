import Mathlib.Probability.CentralLimitTheorem

/-!
# THM-M-0990: obligation-tree composition probe

This module checks the exact root type and the final conditional composition
boundary. The triangular-array characteristic-function bridge remains an
explicit premise for the later proof phase.
-/

noncomputable section

open Filter Finset MeasureTheory ProbabilityTheory
open scoped Real Topology ProbabilityTheory

namespace Stage1Instances.THM_M_0990.ObligationTree

universe u v

/-- Local copies make this standalone validation module elaborate without
adding an unpinned project import. Their bodies mirror `Statement.lean`. -/
def rowVarianceSum {Omega : Type u} [MeasurableSpace Omega]
    (P : Measure Omega) (X : Nat -> Nat -> Omega -> Real) (n : Nat) : Real :=
  ∑ k ∈ Finset.range n, variance (X n k) P

def rowScale {Omega : Type u} [MeasurableSpace Omega]
    (P : Measure Omega) (X : Nat -> Nat -> Omega -> Real) (n : Nat) : Real :=
  Real.sqrt (rowVarianceSum P X n)

def centered {Omega : Type u} [MeasurableSpace Omega]
    (P : Measure Omega) (X : Nat -> Nat -> Omega -> Real)
    (n k : Nat) (omega : Omega) : Real :=
  X n k omega - ∫ x, X n k x ∂P

def lyapunovRatio {Omega : Type u} [MeasurableSpace Omega]
    (P : Measure Omega) (X : Nat -> Nat -> Omega -> Real)
    (delta : Real) (n : Nat) : Real :=
  (Real.rpow (rowScale P X n) (2 + delta))⁻¹ *
    ∑ k ∈ Finset.range n,
      ∫ omega, Real.rpow |centered P X n k omega| (2 + delta) ∂P

def normalizedRowSum {Omega : Type u} [MeasurableSpace Omega]
    (P : Measure Omega) (X : Nat -> Nat -> Omega -> Real)
    (n : Nat) (omega : Omega) : Real :=
  (rowScale P X n)⁻¹ * ∑ k ∈ Finset.range n, centered P X n k omega

def Root : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (Omega' : Type v) [MeasurableSpace Omega']
    (P : Measure Omega) (P' : Measure Omega')
    [IsProbabilityMeasure P] [IsProbabilityMeasure P']
    (X : Nat -> Nat -> Omega -> Real) (Y : Omega' -> Real) (delta : Real),
    HasLaw Y (gaussianReal 0 1) P' ->
    0 < delta ->
    (forall n k : Nat, Measurable (X n k)) ->
    (forall n : Nat, iIndepFun (X n) P) ->
    (forall n k : Nat, MemLp (X n k) 2 P) ->
    (forall n k : Nat,
      Integrable (fun omega => Real.rpow |centered P X n k omega| (2 + delta)) P) ->
    (∀ᶠ n : Nat in atTop,
      0 < rowVarianceSum P X n) ->
    Tendsto (lyapunovRatio P X delta) atTop (nhds 0) ->
    TendstoInDistribution
      (normalizedRowSum P X)
      atTop Y (fun _ : Nat => P) P'

/-- Conditional composition certificate. It checks that the final bridge has
exactly the frozen root type, without assigning unconditional proof credit. -/
theorem root_compose (triangular_array_bridge : Root.{u, v}) : Root.{u, v} :=
  triangular_array_bridge

#check Root
#check root_compose
#print axioms root_compose

end Stage1Instances.THM_M_0990.ObligationTree
