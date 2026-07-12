import Mathlib.MeasureTheory.Function.ConvergenceInDistribution

/-!
# THM-M-1015: exact Slutsky theorem statement

This module freezes the real-valued statement selected at intake. It includes
the pair, sum, product, and nonzero-constant quotient conclusions. It contains
no proof of Slutsky's theorem.
-/

noncomputable section

open Filter MeasureTheory ProbabilityTheory
open scoped Topology ProbabilityTheory

namespace Stage1Instances.THM_M_1015

universe u v w

/-- The four conclusions in the canonical real-valued Slutsky package. -/
def SlutskyConclusions {iota : Type u} {Omega : Type v} {OmegaL : Type w}
    [MeasurableSpace Omega] [MeasurableSpace OmegaL]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (muL : Measure OmegaL) [IsProbabilityMeasure muL] (l : Filter iota)
    (X Y : iota -> Omega -> Real) (Z : OmegaL -> Real) (c : Real) : Prop :=
  TendstoInDistribution (fun n omega => (X n omega, Y n omega)) l
      (fun omega => (Z omega, c)) (fun _ : iota => mu) muL /\
    TendstoInDistribution (fun n omega => X n omega + Y n omega) l
      (fun omega => Z omega + c) (fun _ : iota => mu) muL /\
    TendstoInDistribution (fun n omega => X n omega * Y n omega) l
      (fun omega => Z omega * c) (fun _ : iota => mu) muL /\
    (c != 0 ->
      TendstoInDistribution (fun n omega => X n omega / Y n omega) l
        (fun omega => Z omega / c) (fun _ : iota => mu) muL)

/--
The exact real-valued Slutsky target. The two approximating variables share a
source probability space; the limiting variable may use a different one.
Measurability of `Y n` is explicit because it is required by the pinned
convergence-in-distribution API. The nonzero premise governs only division.
-/
def Statement : Prop :=
  forall (iota : Type u) (Omega : Type v) (OmegaL : Type w)
    [MeasurableSpace Omega] [MeasurableSpace OmegaL]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (muL : Measure OmegaL) [IsProbabilityMeasure muL]
    (l : Filter iota) [l.IsCountablyGenerated]
    (X Y : iota -> Omega -> Real) (Z : OmegaL -> Real) (c : Real),
      TendstoInDistribution X l Z (fun _ : iota => mu) muL ->
      TendstoInMeasure mu Y l (fun _ : Omega => c) ->
      (forall n, AEMeasurable (Y n) mu) ->
      SlutskyConclusions mu muL l X Y Z c

/-- Binder-explicit expansion used as the checked alternate encoding. -/
def ExpandedStatement : Prop :=
  forall (iota : Type u), forall (Omega : Type v), forall (OmegaL : Type w),
    forall (_ : MeasurableSpace Omega), forall (_ : MeasurableSpace OmegaL),
    forall (mu : Measure Omega), forall (_ : IsProbabilityMeasure mu),
    forall (muL : Measure OmegaL), forall (_ : IsProbabilityMeasure muL),
    forall (l : Filter iota), forall (_ : l.IsCountablyGenerated),
    forall (X Y : iota -> Omega -> Real), forall (Z : OmegaL -> Real),
    forall (c : Real),
      TendstoInDistribution X l Z (fun _ : iota => mu) muL ->
      TendstoInMeasure mu Y l (fun _ : Omega => c) ->
      (forall n, AEMeasurable (Y n) mu) ->
      SlutskyConclusions mu muL l X Y Z c

/-- The canonical and explicitly expanded encodings are definitionally equal. -/
theorem statement_iff_expanded : Statement.{u, v, w} <-> ExpandedStatement.{u, v, w} :=
  Iff.rfl

/-! Structural mutations are proposition-valued probes and remain unproved. -/

/-- Mutation: remove the explicit a.e.-measurability premise for `Y`. -/
def mutationRemovedMeasurability : Prop :=
  forall (iota : Type u) (Omega : Type v) (OmegaL : Type w)
    [MeasurableSpace Omega] [MeasurableSpace OmegaL]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (muL : Measure OmegaL) [IsProbabilityMeasure muL]
    (l : Filter iota) [l.IsCountablyGenerated]
    (X Y : iota -> Omega -> Real) (Z : OmegaL -> Real) (c : Real),
      TendstoInDistribution X l Z (fun _ : iota => mu) muL ->
      TendstoInMeasure mu Y l (fun _ : Omega => c) ->
      SlutskyConclusions mu muL l X Y Z c

/-- Mutation: restrict the convergence index domain to natural numbers. -/
def mutationChangedIndexDomain : Prop :=
  forall (Omega : Type v) (OmegaL : Type w)
    [MeasurableSpace Omega] [MeasurableSpace OmegaL]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (muL : Measure OmegaL) [IsProbabilityMeasure muL]
    (l : Filter Nat) [l.IsCountablyGenerated]
    (X Y : Nat -> Omega -> Real) (Z : OmegaL -> Real) (c : Real),
      TendstoInDistribution X l Z (fun _ : Nat => mu) muL ->
      TendstoInMeasure mu Y l (fun _ : Omega => c) ->
      (forall n, AEMeasurable (Y n) mu) ->
      SlutskyConclusions mu muL l X Y Z c

/-- Mutation: choose the limiting constant existentially instead of universally. -/
def mutationChangedConstantScope : Prop :=
  forall (iota : Type u) (Omega : Type v) (OmegaL : Type w)
    [MeasurableSpace Omega] [MeasurableSpace OmegaL]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (muL : Measure OmegaL) [IsProbabilityMeasure muL]
    (l : Filter iota) [l.IsCountablyGenerated]
    (X Y : iota -> Omega -> Real) (Z : OmegaL -> Real),
      exists c : Real,
        TendstoInDistribution X l Z (fun _ : iota => mu) muL ->
        TendstoInMeasure mu Y l (fun _ : Omega => c) ->
        (forall n, AEMeasurable (Y n) mu) ->
        SlutskyConclusions mu muL l X Y Z c

/-- Mutation: demand quotient convergence even at the excluded boundary `c = 0`. -/
def mutationIncludesZeroDenominator : Prop :=
  forall (iota : Type u) (Omega : Type v) (OmegaL : Type w)
    [MeasurableSpace Omega] [MeasurableSpace OmegaL]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (muL : Measure OmegaL) [IsProbabilityMeasure muL]
    (l : Filter iota) [l.IsCountablyGenerated]
    (X Y : iota -> Omega -> Real) (Z : OmegaL -> Real) (c : Real),
      TendstoInDistribution X l Z (fun _ : iota => mu) muL ->
      TendstoInMeasure mu Y l (fun _ : Omega => c) ->
      (forall n, AEMeasurable (Y n) mu) ->
      TendstoInDistribution (fun n omega => (X n omega, Y n omega)) l
          (fun omega => (Z omega, c)) (fun _ : iota => mu) muL /\
        TendstoInDistribution (fun n omega => X n omega + Y n omega) l
          (fun omega => Z omega + c) (fun _ : iota => mu) muL /\
        TendstoInDistribution (fun n omega => X n omega * Y n omega) l
          (fun omega => Z omega * c) (fun _ : iota => mu) muL /\
        TendstoInDistribution (fun n omega => X n omega / Y n omega) l
          (fun omega => Z omega / c) (fun _ : iota => mu) muL

end Stage1Instances.THM_M_1015

set_option pp.explicit true in
#print Stage1Instances.THM_M_1015.Statement
set_option pp.explicit true in
#print Stage1Instances.THM_M_1015.mutationRemovedMeasurability
set_option pp.explicit true in
#print Stage1Instances.THM_M_1015.mutationChangedIndexDomain
set_option pp.explicit true in
#print Stage1Instances.THM_M_1015.mutationChangedConstantScope
set_option pp.explicit true in
#print Stage1Instances.THM_M_1015.mutationIncludesZeroDenominator
