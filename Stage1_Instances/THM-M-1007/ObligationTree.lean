import Mathlib.Probability.Moments.Variance

/-!
# THM-M-1007 conditional obligation composition

This module checks that the two directed three-series implications compose to
the exact fixed-cutoff biconditional. The implications remain explicit
premises, so this file does not prove Kolmogorov's three-series theorem.
-/

noncomputable section

open Filter MeasureTheory ProbabilityTheory Finset
open scoped BigOperators MeasureTheory ProbabilityTheory Topology

namespace Stage1Instances.THM_M_1007.ObligationTree

universe u

def truncate (c : Real) (Z : Omega -> Real) (omega : Omega) : Real :=
  if |Z omega| <= c then Z omega else 0

def SeriesConverges (a : Nat -> Real) : Prop :=
  exists l : Real, Tendsto (fun N => Finset.sum (Finset.range N) a) atTop (nhds l)

def ConvergesAE [MeasurableSpace Omega]
    (mu : Measure Omega) (X : Nat -> Omega -> Real) : Prop :=
  ∀ᵐ omega ∂mu, SeriesConverges (fun n => X n omega)

def ThreeConditions [MeasurableSpace Omega]
    (mu : Measure Omega) (X : Nat -> Omega -> Real) (c : Real) : Prop :=
  Summable (fun n => mu.real {omega | c < |X n omega|}) /\
    SeriesConverges (fun n => integral mu (truncate c (X n))) /\
    Summable (fun n => variance (truncate c (X n)) mu)

def Root : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (X : Nat -> Omega -> Real) (c : Real),
      0 < c ->
      (forall n, Measurable (X n)) ->
      iIndepFun X mu ->
      (ConvergesAE mu X <-> ThreeConditions mu X c)

def Necessity : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (X : Nat -> Omega -> Real) (c : Real),
      0 < c -> (forall n, Measurable (X n)) -> iIndepFun X mu ->
      ConvergesAE mu X -> ThreeConditions mu X c

def Sufficiency : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (X : Nat -> Omega -> Real) (c : Real),
      0 < c -> (forall n, Measurable (X n)) -> iIndepFun X mu ->
      ThreeConditions mu X c -> ConvergesAE mu X

/-- Exact child-to-root composition. No probability theorem is invoked. -/
theorem root_of_directions
    (necessity : Necessity.{u}) (sufficiency : Sufficiency.{u}) : Root.{u} := by
  intro Omega _ mu _ X c hc hmeas hindep
  exact ⟨necessity Omega mu X c hc hmeas hindep,
    sufficiency Omega mu X c hc hmeas hindep⟩

/-- The conditional root expands to the same expression frozen in `Statement.lean`. -/
theorem root_exact_type :
    Root.{u} =
      (forall (Omega : Type u) [MeasurableSpace Omega]
        (mu : Measure Omega) [IsProbabilityMeasure mu]
        (X : Nat -> Omega -> Real) (c : Real),
          0 < c -> (forall n, Measurable (X n)) -> iIndepFun X mu ->
          ((∀ᵐ omega ∂mu, SeriesConverges (fun n => X n omega)) <->
            Summable (fun n => mu.real {omega | c < |X n omega|}) /\
            SeriesConverges (fun n => integral mu (truncate c (X n))) /\
            Summable (fun n => variance (truncate c (X n)) mu))) := by
  rfl

#print root_of_directions
#print axioms root_of_directions

end Stage1Instances.THM_M_1007.ObligationTree
