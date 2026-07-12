import Statement

/-!
# THM-M-1053 conditional obligation composition

This module checks the final composition selected by the frozen architecture.
The pointwise-convergence and ergodic-identification packages remain explicit
premises; this file does not prove Birkhoff's theorem.
-/

open Filter Function MeasureTheory

namespace Stage1.THM_M_1053

universe u

/-- The general (not necessarily ergodic) output of the pointwise theorem. -/
def GeneralInvariantLimitPackage : Prop :=
  forall (X : Type u) (_ : MeasurableSpace X) (mu : Measure X)
    (_ : IsProbabilityMeasure mu) (T : X -> X),
    MeasurePreserving T mu mu -> forall f : X -> Real, Integrable f mu ->
      exists g : X -> Real,
        Integrable g mu /\
        g ∘ T =ᵐ[mu] g /\
        (∀ᵐ x ∂mu, Tendsto (fun n : Nat => timeAverage T f n x) atTop (nhds (g x)))

/-- Identification of any invariant limit with the space integral in the ergodic case. -/
def ErgodicLimitIdentificationPackage : Prop :=
  forall (X : Type u) (_ : MeasurableSpace X) (mu : Measure X)
    (_ : IsProbabilityMeasure mu) (T : X -> X),
    MeasurePreserving T mu mu -> forall (f g : X -> Real),
      Integrable f mu -> Integrable g mu -> g ∘ T =ᵐ[mu] g ->
      Ergodic T mu -> g =ᵐ[mu] fun _ => ∫ x, f x ∂mu

/-- Exact child-to-root composition. Both substantive theorem packages are consumed. -/
theorem statementShape_of_packages
    (general : GeneralInvariantLimitPackage.{u})
    (identify : ErgodicLimitIdentificationPackage.{u}) :
    StatementShape.{u} := by
  intro X _ms mu _prob T hT f hf
  obtain ⟨g, hgInt, hgInv, hgLim⟩ :=
    general X _ mu (inferInstance : IsProbabilityMeasure mu) T hT f hf
  exact ⟨g, hgInt, hgInv, hgLim,
    identify X _ mu (inferInstance : IsProbabilityMeasure mu) T hT f g hf hgInt hgInv⟩

#print axioms statementShape_of_packages

end Stage1.THM_M_1053
