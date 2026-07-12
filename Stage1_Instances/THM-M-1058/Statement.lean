import Mathlib.MeasureTheory.Measure.ProbabilityMeasure
import Mathlib.Topology.Order.LiminfLimsup
import Mathlib.Topology.Semicontinuity.Defs
import Mathlib.Analysis.SpecialFunctions.Log.ENNRealLog

/-!
# THM-M-1058: exact large-deviation-principle statement

This module freezes the full open/closed-set large deviation principle for a
sequence of probability measures. It defines a property of supplied data; it
does not assert that an arbitrary sequence satisfies that property.
-/

noncomputable section

open MeasureTheory Filter
open scoped ENNReal Topology

namespace Stage1Instances.THM_M_1058

universe u

variable (E : Type u) [TopologicalSpace E] [MeasurableSpace E]

/-- Data occurring in the sequence formulation of a large deviation
principle. A good-rate-function compactness condition is deliberately absent. -/
structure LargeDeviationData where
  measures : Nat -> ProbabilityMeasure E
  speed : Nat -> Real
  speed_pos : forall n, 0 < speed n
  speed_tendsto_atTop : Tendsto speed atTop atTop
  rate : E -> EReal
  rate_nonnegative : forall x, (0 : EReal) <= rate x
  rate_lowerSemicontinuous : LowerSemicontinuous rate

/-- The logarithmic probability normalized by the speed. `ENNReal.log` fixes
the boundary convention `log 0 = -infinity`. -/
def scaledLogProbability (D : LargeDeviationData E) (s : Set E) (n : Nat) : EReal :=
  (((D.speed n)⁻¹ : Real) : EReal) * ENNReal.log ((D.measures n : Measure E) s)

/-- Infimum of the rate function over an event. -/
def rateInf (D : LargeDeviationData E) (s : Set E) : EReal :=
  sInf (D.rate '' s)

/-- The full open/closed-set large deviation principle. -/
def LargeDeviationPrinciple (D : LargeDeviationData E) : Prop :=
  (forall F : Set E, IsClosed F ->
      limsup (fun n : Nat => scaledLogProbability E D F n) atTop <= -rateInf E D F) /\
  (forall G : Set E, IsOpen G ->
      -rateInf E D G <= liminf (fun n : Nat => scaledLogProbability E D G n) atTop)

/-- Direct expansion of the intake-selected candidate boundary. -/
def PinnedCandidateSourceShape (D : LargeDeviationData E) : Prop :=
  (forall F : Set E, IsClosed F ->
      limsup (fun n : Nat =>
        (((D.speed n)⁻¹ : Real) : EReal) *
          ENNReal.log ((D.measures n : Measure E) F)) atTop <=
        -sInf (D.rate '' F)) /\
  (forall G : Set E, IsOpen G ->
      -sInf (D.rate '' G) <=
        liminf (fun n : Nat =>
          (((D.speed n)⁻¹ : Real) : EReal) *
            ENNReal.log ((D.measures n : Measure E) G)) atTop)

/-- Checked transport from the direct mathematical expansion to the frozen
Lean predicate. -/
theorem largeDeviationPrinciple_iff_pinnedCandidateSourceShape
    (D : LargeDeviationData E) :
    LargeDeviationPrinciple E D <-> PinnedCandidateSourceShape E D :=
  Iff.rfl

-- Separately elaborated mutations consumed by `check_statement.py`.
structure MutationRemovedSpeedDivergence where
  measures : Nat -> ProbabilityMeasure E
  speed : Nat -> Real
  speed_pos : forall n, 0 < speed n
  rate : E -> EReal
  rate_nonnegative : forall x, (0 : EReal) <= rate x
  rate_lowerSemicontinuous : LowerSemicontinuous rate

def mutationRemovedHypothesis : Type u := MutationRemovedSpeedDivergence E

def mutationChangedDomain : Type :=
  LargeDeviationData Real

def mutationChangedBinderScope (D : LargeDeviationData E) : Prop :=
  forall F : Set E, IsClosed F ->
    (limsup (fun n : Nat => scaledLogProbability E D F n) atTop <= -rateInf E D F /\
      forall G : Set E, IsOpen G ->
        -rateInf E D G <= liminf (fun n : Nat => scaledLogProbability E D G n) atTop)

/-- Boundary mutation: this is the weak-LDP upper bound on compact sets, not
the full closed-set upper bound frozen above. -/
def mutationWeakLDP (D : LargeDeviationData E) : Prop :=
  (forall K : Set E, IsCompact K ->
      limsup (fun n : Nat => scaledLogProbability E D K n) atTop <= -rateInf E D K) /\
  (forall G : Set E, IsOpen G ->
      -rateInf E D G <= liminf (fun n : Nat => scaledLogProbability E D G n) atTop)

end Stage1Instances.THM_M_1058

set_option pp.explicit true in
#print Stage1Instances.THM_M_1058.LargeDeviationPrinciple
