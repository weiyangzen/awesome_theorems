import «Stage1_Instances».«THM-M-1010».ObligationTree

/-!
Executable proof progress for the Skorokhod target.

This file closes the constant-sequence boundary case without assuming the
open general coupling package.  It deliberately does not declare the general
`Target`: weakly convergent nonconstant sequences still require the missing
Skorokhod coupling construction.
-/

noncomputable section

open Filter MeasureTheory ProbabilityTheory Topology

universe u

namespace Stage1Instances.THM_M_1010

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
#print axioms representation_of_constant_laws
#print axioms target_for_constant_sequence

end Stage1Instances.THM_M_1010
