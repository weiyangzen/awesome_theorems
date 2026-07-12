import Mathlib.MeasureTheory.Measure.Tight

/-!
# THM-M-1011: canonical statement of Prokhorov's theorem

This module freezes only the statement boundary. It does not claim proof closure.
-/

open MeasureTheory Set Topology

namespace Stage1Instances.THM_M_1011

universe u

/-- The underlying measures of a family of probability measures. -/
def underlyingMeasures {X : Type u} [MeasurableSpace X]
    (S : Set (ProbabilityMeasure X)) : Set (Measure X) :=
  ((fun P : ProbabilityMeasure X => (P : Measure X)) '' S)

/-- Uniform tightness of a family of probability measures. -/
def IsUniformlyTight {X : Type u} [MeasurableSpace X] [TopologicalSpace X]
    (S : Set (ProbabilityMeasure X)) : Prop :=
  IsTightMeasureSet (underlyingMeasures S)

/--
The exact Stage1 target for Prokhorov's theorem: on a Polish space carrying its
Borel measurable structure, uniform tightness of a family of probability
measures is equivalent to compactness of its closure in mathlib's weak topology.

The explicit pseudo-metric, completeness, and second-countability instances are
mathlib's concrete presentation of the Polish-space hypotheses used by the two
directions of the theorem.
-/
def CanonicalStatement
    (X : Type u) [MeasurableSpace X] [PseudoMetricSpace X] [BorelSpace X]
    [SecondCountableTopology X] [CompleteSpace X] : Prop :=
  forall S : Set (ProbabilityMeasure X),
    IsUniformlyTight S <-> IsCompact (closure S)

/-- Checked unfolding of the frozen target; this gives no proof of the target. -/
theorem canonicalStatement_iff
    (X : Type u) [MeasurableSpace X] [PseudoMetricSpace X] [BorelSpace X]
    [SecondCountableTopology X] [CompleteSpace X] :
    CanonicalStatement X <->
      forall S : Set (ProbabilityMeasure X),
        IsTightMeasureSet
            ((fun P : ProbabilityMeasure X => (P : Measure X)) '' S) <->
          IsCompact (closure S) :=
  Iff.rfl

-- Separately elaborated structural mutations used by `check_statement.py`.
def mutationRemovedCompleteness
    (X : Type u) [MeasurableSpace X] [PseudoMetricSpace X] [BorelSpace X]
    [SecondCountableTopology X] : Prop :=
  forall S : Set (ProbabilityMeasure X),
    IsUniformlyTight S <-> IsCompact (closure S)

def mutationChangedFamilyToSequence
    (X : Type u) [MeasurableSpace X] [PseudoMetricSpace X] [BorelSpace X]
    [SecondCountableTopology X] [CompleteSpace X] : Prop :=
  forall P : Nat -> ProbabilityMeasure X,
    IsUniformlyTight (range P) <-> IsCompact (closure (range P))

def mutationChangedProbabilityToFiniteMeasures
    (X : Type u) [MeasurableSpace X] [PseudoMetricSpace X] [BorelSpace X]
    [SecondCountableTopology X] [CompleteSpace X] : Prop :=
  forall S : Set (FiniteMeasure X), IsCompact (closure S)

def mutationOneDirectionOnly
    (X : Type u) [MeasurableSpace X] [PseudoMetricSpace X] [BorelSpace X]
    [SecondCountableTopology X] [CompleteSpace X] : Prop :=
  forall S : Set (ProbabilityMeasure X),
    IsUniformlyTight S -> IsCompact (closure S)

end Stage1Instances.THM_M_1011

set_option pp.explicit true in
#print Stage1Instances.THM_M_1011.CanonicalStatement
