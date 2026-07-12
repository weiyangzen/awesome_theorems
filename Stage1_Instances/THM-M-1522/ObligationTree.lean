import Statement

/-!
# THM-M-1522 conditional obligation composition

This module checks the final logical composition selected by the frozen
architecture. The two substantive Birkhoff packages remain hypotheses; this
does not prove the pointwise ergodic theorem.
-/

open Filter MeasureTheory
open scoped Topology

namespace Stage1Instances.THM_M_1522

universe u

/-- Data furnished by the general pointwise theorem before ergodicity is used
to identify the limit. -/
def InvariantLimitData {X : Type u} [MeasurableSpace X]
    (mu : Measure X) (T : X -> X) (f g : X -> Real) : Prop :=
  Integrable g mu /\
    (∀ᵐ x ∂mu, g (T x) = g x) /\
      integral mu g = integral mu f

/-- The general pointwise package, deliberately kept as an open premise. -/
def GeneralPointwiseLimitPackage : Prop :=
  forall (X : Type u) [MeasurableSpace X] (mu : Measure X)
    [IsProbabilityMeasure mu] (T : X -> X) (f : X -> Real),
      Ergodic T mu -> Integrable f mu ->
        exists g : X -> Real,
          (∀ᵐ x ∂mu, Tendsto (fun n : Nat => birkhoffAverage Real T f n x)
            atTop (nhds (g x))) /\
          InvariantLimitData mu T f g

/-- The ergodic identification package, also left as an open premise. -/
def ErgodicInvariantLimitIdentification : Prop :=
  forall (X : Type u) [MeasurableSpace X] (mu : Measure X)
    [IsProbabilityMeasure mu] (T : X -> X) (f g : X -> Real),
      Ergodic T mu -> Integrable f mu -> InvariantLimitData mu T f g ->
        ∀ᵐ x ∂mu, g x = integral mu f

/-- Checked conditional composition into the exact canonical target. -/
theorem root_of_pointwise_and_identification
    (pointwise : GeneralPointwiseLimitPackage.{u})
    (identify : ErgodicInvariantLimitIdentification.{u}) :
    BirkhoffPointwiseErgodicTarget.{u} := by
  intro X _ mu _ T f hT hf
  obtain ⟨g, hlimit, hdata⟩ := pointwise X mu T f hT hf
  have hidentify := identify X mu T f g hT hf hdata
  filter_upwards [hlimit, hidentify] with x hx hgx
  simpa only [hgx] using hx

#print axioms root_of_pointwise_and_identification

end Stage1Instances.THM_M_1522
