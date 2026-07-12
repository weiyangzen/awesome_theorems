import Mathlib.Probability.HasLaw
import Mathlib.MeasureTheory.Measure.LevyProkhorovMetric
import Mathlib.MeasureTheory.Constructions.Polish.Basic

noncomputable section

open Filter MeasureTheory ProbabilityTheory Topology

universe u

namespace Stage1Instances.THM_M_1010

/-- Weak convergence in the pinned mathlib topology on Borel probability measures. -/
def WeakConvergence {S : Type u} [TopologicalSpace S] [MeasurableSpace S]
    [BorelSpace S] (muSeq : Nat -> ProbabilityMeasure S)
    (mu : ProbabilityMeasure S) : Prop :=
  Tendsto muSeq atTop (nhds mu)

/-- A common probability-space realization with the requested laws and a.s. convergence. -/
structure Representation
    (S : Type u) [TopologicalSpace S] [MeasurableSpace S]
    (muSeq : Nat -> ProbabilityMeasure S) (mu : ProbabilityMeasure S) : Type (u + 1) where
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

/-- Exact Polish-space form of the Skorokhod representation theorem. -/
def Target
    (S : Type u) [TopologicalSpace S] [MeasurableSpace S]
    [BorelSpace S] [PolishSpace S] : Prop :=
  forall (muSeq : Nat -> ProbabilityMeasure S) (mu : ProbabilityMeasure S),
    WeakConvergence muSeq mu -> Nonempty (Representation S muSeq mu)

/-- Checked expansion used to relate the named target to its explicit binder form. -/
theorem target_iff_expanded
    (S : Type u) [TopologicalSpace S] [MeasurableSpace S]
    [BorelSpace S] [PolishSpace S] :
    Target S <->
      forall (muSeq : Nat -> ProbabilityMeasure S) (mu : ProbabilityMeasure S),
        WeakConvergence muSeq mu -> Nonempty (Representation S muSeq mu) :=
  Iff.rfl

end Stage1Instances.THM_M_1010
