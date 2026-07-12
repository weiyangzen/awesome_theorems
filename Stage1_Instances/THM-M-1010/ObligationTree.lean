import «Stage1_Instances».«THM-M-1010».Statement

/-!
Checked conditional composition for the frozen Skorokhod proof architecture.
`CouplingPackage` is deliberately left as an explicit premise: this module
checks only that its fields assemble the exact canonical target.
-/

noncomputable section

open Filter MeasureTheory ProbabilityTheory Topology

universe u

namespace Stage1Instances.THM_M_1010.ObligationTree

/-- Data produced by the still-open coupling construction for one weakly
convergent sequence. -/
structure CouplingData
    (S : Type u) [TopologicalSpace S] [MeasurableSpace S]
    (muSeq : Nat -> ProbabilityMeasure S) (mu : ProbabilityMeasure S) where
  sample : Type u
  sampleMeasurable : MeasurableSpace sample
  probability : Measure sample
  isProbability : IsProbabilityMeasure probability
  seqVar : Nat -> sample -> S
  limitVar : sample -> S
  seq_hasLaw : forall n, HasLaw (seqVar n) (muSeq n : Measure S) probability
  limit_hasLaw : HasLaw limitVar (mu : Measure S) probability
  ae_tendsto :
    ∀ᵐ omega ∂probability,
      Tendsto (fun n => seqVar n omega) atTop (nhds (limitVar omega))

/-- Exact open construction package, quantified over precisely the inputs of
the canonical target. -/
def CouplingPackage
    (S : Type u) [TopologicalSpace S] [MeasurableSpace S]
    [BorelSpace S] [PolishSpace S] : Prop :=
  forall (muSeq : Nat -> ProbabilityMeasure S) (mu : ProbabilityMeasure S),
    WeakConvergence muSeq mu -> Nonempty (CouplingData S muSeq mu)

/-- No mathematical content is hidden in the final conversion: all fields of
the construction package are consumed by the canonical `Representation`. -/
def CouplingData.toRepresentation
    {S : Type u} [TopologicalSpace S] [MeasurableSpace S]
    {muSeq : Nat -> ProbabilityMeasure S} {mu : ProbabilityMeasure S}
    (data : CouplingData S muSeq mu) : Representation S muSeq mu where
  sample := data.sample
  sampleMeasurable := data.sampleMeasurable
  probability := data.probability
  isProbability := data.isProbability
  seqVar := data.seqVar
  limitVar := data.limitVar
  seq_hasLaw := data.seq_hasLaw
  limit_hasLaw := data.limit_hasLaw
  ae_tendsto := data.ae_tendsto

/-- Checked child-to-parent composition into the exact frozen target. -/
theorem target_of_couplingPackage
    (S : Type u) [TopologicalSpace S] [MeasurableSpace S]
    [BorelSpace S] [PolishSpace S] (package : CouplingPackage S) : Target S := by
  intro muSeq mu hweak
  obtain ⟨data⟩ := package muSeq mu hweak
  exact ⟨data.toRepresentation⟩

#check target_of_couplingPackage
#print axioms target_of_couplingPackage

end Stage1Instances.THM_M_1010.ObligationTree
