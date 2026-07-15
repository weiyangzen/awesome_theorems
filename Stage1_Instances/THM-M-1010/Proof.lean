import «Stage1_Instances».«THM-M-1010».ObligationTree
import Mathlib.Probability.HasLawExists

/-!
Executable proof progress for the Skorokhod target.

This file realizes all prescribed marginals measurably on one sample space
and closes the constant-sequence boundary case. It deliberately does not
declare the general `Target`: weakly convergent nonconstant sequences still
require the missing convergence-compatible Skorokhod coupling construction.
-/

noncomputable section

open Filter MeasureTheory ProbabilityTheory Topology

universe u

namespace Stage1Instances.THM_M_1010

/-- All prescribed marginals realized on one probability space. This is the
exact data needed before the still-open almost-sure convergence field can be
added. -/
structure CommonMarginalData
    (S : Type u) [MeasurableSpace S]
    (muSeq : Nat -> ProbabilityMeasure S) (mu : ProbabilityMeasure S) : Type (u + 1) where
  sample : Type u
  sampleMeasurable : MeasurableSpace sample
  probability : Measure sample
  isProbability : IsProbabilityMeasure probability
  seqVar : Nat -> sample -> S
  limitVar : sample -> S
  seq_measurable : forall n, @Measurable sample S sampleMeasurable _ (seqVar n)
  limit_measurable : @Measurable sample S sampleMeasurable _ limitVar
  seq_hasLaw : forall n,
    @HasLaw sample S sampleMeasurable _ (seqVar n) (muSeq n : Measure S) probability
  limit_hasLaw : @HasLaw sample S sampleMeasurable _ limitVar (mu : Measure S) probability

/-- A single universe-correct probability space carries measurable random
variables with every prescribed law. No convergence relation is claimed. -/
theorem exists_common_space_exact_marginals
    (S : Type u) [MeasurableSpace S]
    (muSeq : Nat -> ProbabilityMeasure S) (mu : ProbabilityMeasure S) :
    Nonempty (CommonMarginalData S muSeq mu) := by
  let law : Option Nat -> Measure S
    | none => mu
    | some n => muSeq n
  haveI (i : Option Nat) : IsProbabilityMeasure (law i) := by
    cases i <;> simp only [law] <;> infer_instance
  obtain ⟨Omega, omegaMeasurable, probability, randomVar, hmeasurable, hlaw, _, hprobability⟩ :=
    exists_hasLaw_indepFun (fun _ : Option Nat => S) law
  letI : MeasurableSpace Omega := omegaMeasurable
  exact ⟨{
    sample := Omega
    sampleMeasurable := omegaMeasurable
    probability := probability
    isProbability := hprobability
    seqVar := fun n => randomVar (some n)
    limitVar := randomVar none
    seq_measurable := fun n => hmeasurable (some n)
    limit_measurable := hmeasurable none
    seq_hasLaw := fun n => by simpa [law] using hlaw (some n)
    limit_hasLaw := by simpa [law] using hlaw none
  }⟩

/-- A sequence whose laws are all the limit law has the required common-space
representation, using the target space itself and the identity random
variable. -/
theorem representation_of_constant_laws
    (S : Type u) [TopologicalSpace S] [MeasurableSpace S]
    (mu : ProbabilityMeasure S) :
    Nonempty (Representation S (fun _ => mu) mu) := by
  let probability : Measure S := mu
  haveI : IsProbabilityMeasure probability := inferInstance
  refine ⟨{
    sample := S
    sampleMeasurable := inferInstance
    probability := probability
    isProbability := inferInstance
    seqVar := fun _ => id
    limitVar := id
    seq_hasLaw := ?_
    limit_hasLaw := ?_
    ae_tendsto := ?_
  }⟩
  · intro n
    exact HasLaw.id
  · exact HasLaw.id
  · filter_upwards with omega
    exact tendsto_const_nhds

/-- Checked boundary corollary in the exact representation language. -/
theorem target_for_constant_sequence
    (S : Type u) [TopologicalSpace S] [MeasurableSpace S]
    [BorelSpace S] [PolishSpace S] (mu : ProbabilityMeasure S) :
    WeakConvergence (fun _ => mu) mu ->
      Nonempty (Representation S (fun _ => mu) mu) := by
  intro _
  exact representation_of_constant_laws S mu

#check representation_of_constant_laws
#check target_for_constant_sequence
#check exists_common_space_exact_marginals
#print axioms representation_of_constant_laws
#print axioms target_for_constant_sequence
#print axioms exists_common_space_exact_marginals

end Stage1Instances.THM_M_1010
