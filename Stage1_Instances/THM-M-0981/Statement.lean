import Mathlib.MeasureTheory.Measure.ProbabilityMeasure

/-!
# THM-M-0981: exact Kolmogorov-axioms statement

This module freezes and tests the statement boundary only. The proof that the
clauses hold for mathlib probability measures belongs to a later phase.
-/

open Function MeasureTheory Set

namespace Stage1Instances.THM_M_0981

universe u

/-- The normalized empty-event, unit-mass, and countable-additivity clauses. -/
def KolmogorovAxioms {Omega : Type u} [MeasurableSpace Omega]
    (P : Measure Omega) : Prop :=
  P ∅ = 0 /\
    P univ = 1 /\
      forall A : Nat -> Set Omega,
        (forall n, MeasurableSet (A n)) ->
          Pairwise (Disjoint on A) ->
            P (iUnion A) = tsum (fun n => P (A n))

/-- The exact intake-selected target: every normalized measure has the explicit
Kolmogorov clauses. The sample type remains an explicit parameter so the
declaration is universe-polymorphic. -/
def KolmogorovAxiomsTarget (Omega : Type u) [MeasurableSpace Omega] : Prop :=
  forall P : Measure Omega, IsProbabilityMeasure P -> KolmogorovAxioms P

/-- The historical candidate expanded locally, without importing its broad
probability and stochastic-process dependency surface. -/
def PinnedCandidateSourceShape (Omega : Type u) [MeasurableSpace Omega] : Prop :=
  forall P : Measure Omega, IsProbabilityMeasure P ->
    P ∅ = 0 /\
      P univ = 1 /\
        forall A : Nat -> Set Omega,
          (forall n, MeasurableSet (A n)) ->
            Pairwise (Disjoint on A) ->
              P (iUnion A) = tsum (fun n => P (A n))

/-- Checked expansion of the historical candidate statement. -/
theorem target_iff_pinnedCandidateSourceShape
    (Omega : Type u) [MeasurableSpace Omega] :
    KolmogorovAxiomsTarget Omega <-> PinnedCandidateSourceShape Omega := by
  rfl

/-- Equivalent subtype packaging of the normalized-measure premise. -/
def ProbabilityMeasurePackaging (Omega : Type u) [MeasurableSpace Omega] : Prop :=
  forall P : ProbabilityMeasure Omega, KolmogorovAxioms (P : Measure Omega)

/-- Checked transport between class-premise and subtype packaging. -/
theorem target_iff_probabilityMeasurePackaging
    (Omega : Type u) [MeasurableSpace Omega] :
    KolmogorovAxiomsTarget Omega <-> ProbabilityMeasurePackaging Omega := by
  constructor
  · intro h P
    exact h (P : Measure Omega) P.prop
  · intro h P hP
    exact h (show ProbabilityMeasure Omega from ⟨P, hP⟩)

-- Separately elaborated, deliberately non-equivalent structural mutations.
def mutationRemovedMeasurability (Omega : Type u) [MeasurableSpace Omega] : Prop :=
  forall P : Measure Omega, IsProbabilityMeasure P ->
    forall A : Nat -> Set Omega, Pairwise (Disjoint on A) ->
      P (iUnion A) = tsum (fun n => P (A n))

def mutationChangedEventDomain (Omega : Type u) [MeasurableSpace Omega] : Prop :=
  forall P : Measure Omega, IsProbabilityMeasure P ->
    forall A : Fin 2 -> Set Omega,
      (forall n, MeasurableSet (A n)) -> Pairwise (Disjoint on A) ->
        P (A 0 ∪ A 1) = P (A 0) + P (A 1)

def mutationChangedBinderScope (Omega : Type u) [MeasurableSpace Omega] : Prop :=
  forall P : Measure Omega, IsProbabilityMeasure P ->
    exists A : Nat -> Set Omega,
      (forall n, MeasurableSet (A n)) /\ Pairwise (Disjoint on A) /\
        P (iUnion A) = tsum (fun n => P (A n))

def mutationRemovedNormalization (Omega : Type u) [MeasurableSpace Omega] : Prop :=
  forall P : Measure Omega, KolmogorovAxioms P

/-- The empty family is retained by the universal event-family binder. -/
theorem emptyFamilyBoundary {Omega : Type u} [MeasurableSpace Omega] :
    (fun _n : Nat => (∅ : Set Omega)) = fun _n => ∅ := by
  rfl

end Stage1Instances.THM_M_0981

set_option pp.explicit true in
#print Stage1Instances.THM_M_0981.KolmogorovAxiomsTarget
