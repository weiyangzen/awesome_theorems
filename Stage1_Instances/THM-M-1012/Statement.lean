import Mathlib.MeasureTheory.Measure.CharacteristicFunction.Basic
import Mathlib.MeasureTheory.Measure.ProbabilityMeasure

/-!
# THM-M-1012: exact Levy continuity statement

This module freezes the known-limit equivalence selected at intake. It does not
prove Levy's continuity theorem.
-/

noncomputable section

open Filter MeasureTheory
open scoped Topology RealInnerProductSpace

namespace Stage1Instances.THM_M_1012

universe u

/-- The known-limit form of Levy's continuity theorem: weak convergence of
probability measures is equivalent to pointwise convergence of characteristic
functions to the characteristic function of the specified limiting measure. -/
def LevyContinuityKnownLimitTarget : Prop :=
  forall (E : Type u) [NormedAddCommGroup E] [InnerProductSpace Real E]
    [FiniteDimensional Real E] [MeasurableSpace E] [BorelSpace E]
    (mu : Nat -> ProbabilityMeasure E) (mu0 : ProbabilityMeasure E),
      Tendsto mu atTop (nhds mu0) <->
        forall t : E,
          Tendsto (fun n : Nat => charFun ((mu n : ProbabilityMeasure E) : Measure E) t) atTop
            (nhds (charFun ((mu0 : ProbabilityMeasure E) : Measure E) t))

/-- A binder-explicit encoding used to check the canonical target directly. -/
def ExpandedKnownLimitTarget : Prop :=
  forall (E : Type u) [NormedAddCommGroup E] [InnerProductSpace Real E]
    [FiniteDimensional Real E] [MeasurableSpace E] [BorelSpace E],
    forall (mu : Nat -> ProbabilityMeasure E),
    forall (mu0 : ProbabilityMeasure E),
      Tendsto mu atTop (nhds mu0) <->
        forall t : E,
          Tendsto (fun n : Nat => charFun ((mu n : ProbabilityMeasure E) : Measure E) t) atTop
            (nhds (charFun ((mu0 : ProbabilityMeasure E) : Measure E) t))

/-- Checked transport to the binder-explicit encoding. -/
theorem target_iff_expanded :
    LevyContinuityKnownLimitTarget.{u} <-> ExpandedKnownLimitTarget.{u} :=
  by simp only [LevyContinuityKnownLimitTarget, ExpandedKnownLimitTarget]

-- Separately elaborated, deliberately non-equivalent structural mutations.
def mutationRemovedFiniteDimensional : Prop :=
  forall (E : Type u) [NormedAddCommGroup E] [InnerProductSpace Real E]
    [MeasurableSpace E] [BorelSpace E]
    (mu : Nat -> ProbabilityMeasure E) (mu0 : ProbabilityMeasure E),
      Tendsto mu atTop (nhds mu0) <->
        forall t : E,
          Tendsto (fun n : Nat => charFun ((mu n : ProbabilityMeasure E) : Measure E) t) atTop
            (nhds (charFun ((mu0 : ProbabilityMeasure E) : Measure E) t))

def mutationChangedDomainToReal : Prop :=
  forall (mu : Nat -> ProbabilityMeasure Real) (mu0 : ProbabilityMeasure Real),
    Tendsto mu atTop (nhds mu0) <->
      forall t : Real,
        Tendsto (fun n : Nat => charFun ((mu n : ProbabilityMeasure Real) : Measure Real) t) atTop
          (nhds (charFun ((mu0 : ProbabilityMeasure Real) : Measure Real) t))

def mutationChangedBinderScope : Prop :=
  forall (E : Type u) [NormedAddCommGroup E] [InnerProductSpace Real E]
    [FiniteDimensional Real E] [MeasurableSpace E] [BorelSpace E]
    (mu : Nat -> ProbabilityMeasure E),
      exists mu0 : ProbabilityMeasure E,
        Tendsto mu atTop (nhds mu0) <->
          forall t : E,
            Tendsto (fun n : Nat => charFun ((mu n : ProbabilityMeasure E) : Measure E) t) atTop
              (nhds (charFun ((mu0 : ProbabilityMeasure E) : Measure E) t))

def mutationOnlyNonzeroFrequencies : Prop :=
  forall (E : Type u) [NormedAddCommGroup E] [InnerProductSpace Real E]
    [FiniteDimensional Real E] [MeasurableSpace E] [BorelSpace E]
    (mu : Nat -> ProbabilityMeasure E) (mu0 : ProbabilityMeasure E),
      Tendsto mu atTop (nhds mu0) <->
        forall t : E, Not (t = 0) ->
          Tendsto (fun n : Nat => charFun ((mu n : ProbabilityMeasure E) : Measure E) t) atTop
            (nhds (charFun ((mu0 : ProbabilityMeasure E) : Measure E) t))

/-- The target includes the zero-dimensional finite-dimensional space. -/
def zeroDimensionalBoundary : Prop :=
  forall (mu : Nat -> ProbabilityMeasure (EuclideanSpace Real (Fin 0)))
    (mu0 : ProbabilityMeasure (EuclideanSpace Real (Fin 0))),
      Tendsto mu atTop (nhds mu0) <->
        forall t : EuclideanSpace Real (Fin 0),
          Tendsto (fun n : Nat => charFun ((mu n : ProbabilityMeasure (EuclideanSpace Real (Fin 0))) : Measure (EuclideanSpace Real (Fin 0))) t) atTop
            (nhds (charFun ((mu0 : ProbabilityMeasure (EuclideanSpace Real (Fin 0))) : Measure (EuclideanSpace Real (Fin 0))) t))

end Stage1Instances.THM_M_1012

set_option pp.explicit true in
#print Stage1Instances.THM_M_1012.LevyContinuityKnownLimitTarget
