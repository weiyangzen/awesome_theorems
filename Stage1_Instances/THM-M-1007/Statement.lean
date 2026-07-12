import Mathlib.Probability.Moments.Variance

/-!
# THM-M-1007: Kolmogorov three-series theorem statement

This module freezes the real-valued, fixed-positive-cutoff biconditional selected at intake.
It defines and probes the proposition only; it does not prove the three-series theorem.
-/

noncomputable section

open Filter MeasureTheory ProbabilityTheory Finset
open scoped BigOperators MeasureTheory ProbabilityTheory Topology

namespace Stage1Instances.THM_M_1007

universe u

/-- Truncation at the inclusive cutoff selected by the intake record. -/
def truncate (c : Real) (Z : Omega -> Real) (omega : Omega) : Real :=
  if |Z omega| <= c then Z omega else 0

/-- Sequential convergence of a real series, rather than mathlib's unconditional `Summable`.
This distinction is material for the (possibly conditionally convergent) centered-mean series. -/
def SeriesConverges (a : Nat -> Real) : Prop :=
  exists l : Real, Tendsto (fun N => Finset.sum (Finset.range N) a) atTop (nhds l)

/-- The exact fixed-cutoff form of Kolmogorov's three-series theorem selected at intake. -/
def KolmogorovThreeSeriesTarget : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (X : Nat -> Omega -> Real) (c : Real),
      0 < c ->
      (forall n, Measurable (X n)) ->
      iIndepFun X mu ->
      ((∀ᵐ omega ∂mu, SeriesConverges (fun n => X n omega)) <->
        Summable (fun n => mu.real {omega | c < |X n omega|}) /\
        SeriesConverges (fun n => integral mu (truncate c (X n))) /\
        Summable (fun n => variance (truncate c (X n)) mu))

/-- A stable intake-facing alias for the canonical target. -/
def ExpandedIntakeShape : Prop := KolmogorovThreeSeriesTarget.{u}

theorem target_iff_expandedIntakeShape :
    KolmogorovThreeSeriesTarget.{u} <-> ExpandedIntakeShape.{u} := by
  rfl

-- Separately elaborated, deliberately non-equivalent statement mutations.
def mutationRemovedMeasurability : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (X : Nat -> Omega -> Real) (c : Real),
      0 < c -> iIndepFun X mu ->
      ((∀ᵐ omega ∂mu, SeriesConverges (fun n => X n omega)) <->
        Summable (fun n => mu.real {omega | c < |X n omega|}) /\
        SeriesConverges (fun n => integral mu (truncate c (X n))) /\
        Summable (fun n => variance (truncate c (X n)) mu))

def mutationRemovedIndependence : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (X : Nat -> Omega -> Real) (c : Real),
      0 < c -> (forall n, Measurable (X n)) ->
      ((∀ᵐ omega ∂mu, SeriesConverges (fun n => X n omega)) <->
        Summable (fun n => mu.real {omega | c < |X n omega|}) /\
        SeriesConverges (fun n => integral mu (truncate c (X n))) /\
        Summable (fun n => variance (truncate c (X n)) mu))

def mutationChangedBinderScope : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (X : Nat -> Omega -> Real),
      (forall c : Real, 0 < c) ->
      (forall n, Measurable (X n)) -> iIndepFun X mu ->
      forall c : Real,
        ((∀ᵐ omega ∂mu, SeriesConverges (fun n => X n omega)) <->
          Summable (fun n => mu.real {omega | c < |X n omega|}) /\
          SeriesConverges (fun n => integral mu (truncate c (X n))) /\
          Summable (fun n => variance (truncate c (X n)) mu))

def mutationNonnegativeCutoff : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (X : Nat -> Omega -> Real) (c : Real),
      0 <= c -> (forall n, Measurable (X n)) -> iIndepFun X mu ->
      ((∀ᵐ omega ∂mu, SeriesConverges (fun n => X n omega)) <->
        Summable (fun n => mu.real {omega | c < |X n omega|}) /\
        SeriesConverges (fun n => integral mu (truncate c (X n))) /\
        Summable (fun n => variance (truncate c (X n)) mu))

/-- Values exactly at the cutoff are retained by the selected inclusive truncation. -/
theorem truncate_eq_self_of_abs_le {c x : Real} (h : |x| <= c) :
    truncate c (fun _ : Unit => x) () = x := by
  simp [truncate, h]

/-- Values strictly beyond the cutoff are removed. -/
theorem truncate_eq_zero_of_lt_abs {c x : Real} (h : c < |x|) :
    truncate c (fun _ : Unit => x) () = 0 := by
  simp [truncate, not_le_of_gt h]

end Stage1Instances.THM_M_1007

set_option pp.explicit true in
#print Stage1Instances.THM_M_1007.KolmogorovThreeSeriesTarget
