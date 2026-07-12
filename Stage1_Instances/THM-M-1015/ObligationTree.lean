import Mathlib.MeasureTheory.Function.ConvergenceInDistribution

/-!
# THM-M-1015 conditional obligation composition

The four conclusion branches are explicit premises. This file checks their
composition into the exact Slutsky package; it does not prove those premises.
-/

noncomputable section

open Filter MeasureTheory ProbabilityTheory
open scoped Topology ProbabilityTheory

namespace Stage1Instances.THM_M_1015.ObligationTree

universe u v w

variable {iota : Type u} {Omega : Type v} {OmegaL : Type w}
  [MeasurableSpace Omega] [MeasurableSpace OmegaL]
  (mu : Measure Omega) [IsProbabilityMeasure mu]
  (muL : Measure OmegaL) [IsProbabilityMeasure muL]
  (l : Filter iota) [l.IsCountablyGenerated]
  (X Y : iota -> Omega -> Real) (Z : OmegaL -> Real) (c : Real)

def PairBranch : Prop :=
  TendstoInDistribution (fun n omega => (X n omega, Y n omega)) l
    (fun omega => (Z omega, c)) (fun _ : iota => mu) muL

def AddBranch : Prop :=
  TendstoInDistribution (fun n omega => X n omega + Y n omega) l
    (fun omega => Z omega + c) (fun _ : iota => mu) muL

def MulBranch : Prop :=
  TendstoInDistribution (fun n omega => X n omega * Y n omega) l
    (fun omega => Z omega * c) (fun _ : iota => mu) muL

def QuotBranch : Prop :=
  c != 0 -> TendstoInDistribution (fun n omega => X n omega / Y n omega) l
    (fun omega => Z omega / c) (fun _ : iota => mu) muL

def Conclusions : Prop :=
  PairBranch mu muL l X Y Z c /\ AddBranch mu muL l X Y Z c /\
    MulBranch mu muL l X Y Z c /\ QuotBranch mu muL l X Y Z c

def Root : Prop :=
  forall (iota : Type u) (Omega : Type v) (OmegaL : Type w)
    [MeasurableSpace Omega] [MeasurableSpace OmegaL]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (muL : Measure OmegaL) [IsProbabilityMeasure muL]
    (l : Filter iota) [l.IsCountablyGenerated]
    (X Y : iota -> Omega -> Real) (Z : OmegaL -> Real) (c : Real),
      TendstoInDistribution X l Z (fun _ : iota => mu) muL ->
      TendstoInMeasure mu Y l (fun _ : Omega => c) ->
      (forall n, AEMeasurable (Y n) mu) ->
      Conclusions mu muL l X Y Z c

/-- Exact child-to-root composition. Every branch premise is consumed. -/
theorem root_compose
    (pair : forall (iota : Type u) (Omega : Type v) (OmegaL : Type w)
      [MeasurableSpace Omega] [MeasurableSpace OmegaL]
      (mu : Measure Omega) [IsProbabilityMeasure mu]
      (muL : Measure OmegaL) [IsProbabilityMeasure muL]
      (l : Filter iota) [l.IsCountablyGenerated]
      (X Y : iota -> Omega -> Real) (Z : OmegaL -> Real) (c : Real),
        TendstoInDistribution X l Z (fun _ : iota => mu) muL ->
        TendstoInMeasure mu Y l (fun _ : Omega => c) ->
        (forall n, AEMeasurable (Y n) mu) -> PairBranch mu muL l X Y Z c)
    (add : forall (iota : Type u) (Omega : Type v) (OmegaL : Type w)
      [MeasurableSpace Omega] [MeasurableSpace OmegaL]
      (mu : Measure Omega) [IsProbabilityMeasure mu]
      (muL : Measure OmegaL) [IsProbabilityMeasure muL]
      (l : Filter iota) [l.IsCountablyGenerated]
      (X Y : iota -> Omega -> Real) (Z : OmegaL -> Real) (c : Real),
        TendstoInDistribution X l Z (fun _ : iota => mu) muL ->
        TendstoInMeasure mu Y l (fun _ : Omega => c) ->
        (forall n, AEMeasurable (Y n) mu) -> AddBranch mu muL l X Y Z c)
    (mul : forall (iota : Type u) (Omega : Type v) (OmegaL : Type w)
      [MeasurableSpace Omega] [MeasurableSpace OmegaL]
      (mu : Measure Omega) [IsProbabilityMeasure mu]
      (muL : Measure OmegaL) [IsProbabilityMeasure muL]
      (l : Filter iota) [l.IsCountablyGenerated]
      (X Y : iota -> Omega -> Real) (Z : OmegaL -> Real) (c : Real),
        TendstoInDistribution X l Z (fun _ : iota => mu) muL ->
        TendstoInMeasure mu Y l (fun _ : Omega => c) ->
        (forall n, AEMeasurable (Y n) mu) -> MulBranch mu muL l X Y Z c)
    (quot : forall (iota : Type u) (Omega : Type v) (OmegaL : Type w)
      [MeasurableSpace Omega] [MeasurableSpace OmegaL]
      (mu : Measure Omega) [IsProbabilityMeasure mu]
      (muL : Measure OmegaL) [IsProbabilityMeasure muL]
      (l : Filter iota) [l.IsCountablyGenerated]
      (X Y : iota -> Omega -> Real) (Z : OmegaL -> Real) (c : Real),
        TendstoInDistribution X l Z (fun _ : iota => mu) muL ->
        TendstoInMeasure mu Y l (fun _ : Omega => c) ->
        (forall n, AEMeasurable (Y n) mu) -> QuotBranch mu muL l X Y Z c) :
    Root.{u, v, w} := by
  intro iota Omega OmegaL _ _ mu _ muL _ l _ X Y Z c hXZ hY hYmeas
  exact ⟨pair iota Omega OmegaL mu muL l X Y Z c hXZ hY hYmeas,
    add iota Omega OmegaL mu muL l X Y Z c hXZ hY hYmeas,
    mul iota Omega OmegaL mu muL l X Y Z c hXZ hY hYmeas,
    quot iota Omega OmegaL mu muL l X Y Z c hXZ hY hYmeas⟩

#check MeasureTheory.TendstoInDistribution.prodMk_of_tendstoInMeasure_const
#check MeasureTheory.TendstoInDistribution.add_of_tendstoInMeasure_const
#check MeasureTheory.TendstoInDistribution.continuous_comp_prodMk_of_tendstoInMeasure_const
#print axioms root_compose

end Stage1Instances.THM_M_1015.ObligationTree
