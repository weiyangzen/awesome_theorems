import «Stage1_Instances».«THM-M-0996».Statement

/-!
# THM-M-0996 conditional obligation composition

This file checks only the terminal composition chosen by the frozen obligation
architecture.  It deliberately takes the two central Gaussian estimates as
premises; neither premise is asserted or proved here.
-/

noncomputable section

open MeasureTheory ProbabilityTheory

namespace Stage1Instances.THM_M_0996

universe u

/-- A profile-free interface for the half-space calculation.  The proof phase
must instantiate `profile` and prove this equality; this declaration does not
choose an inverse-CDF endpoint convention. -/
def HalfspaceEnlargementFormula
    {E : Type u} [NormedAddCommGroup E] [InnerProductSpace Real E]
    [MeasurableSpace E] [BorelSpace E] [FiniteDimensional Real E]
    (profile : ENNReal -> Real -> ENNReal) : Prop :=
  forall (H : Set E), IsUnitHalfspace H -> forall r : Real, 0 < r ->
    stdGaussian E (Metric.thickening r H) = profile (stdGaussian E H) r

/-- The substantive arbitrary-set estimate.  This is an open premise, not a
repo-local proof of Gaussian isoperimetry. -/
def GeneralSetEnlargementBound
    {E : Type u} [NormedAddCommGroup E] [InnerProductSpace Real E]
    [MeasurableSpace E] [BorelSpace E] [FiniteDimensional Real E]
    (profile : ENNReal -> Real -> ENNReal) : Prop :=
  forall (A : Set E), MeasurableSet A -> forall r : Real, 0 < r ->
    profile (stdGaussian E A) r <= stdGaussian E (Metric.thickening r A)

/-- Checked child-to-parent composition.  It consumes both central children,
uses the equal-measure hypothesis to align their profile arguments, and yields
the exact statement-phase target. -/
theorem target_of_profile_bounds
    (profile : ENNReal -> Real -> ENNReal)
    (hHalfspace : forall (E : Type u) [NormedAddCommGroup E]
      [InnerProductSpace Real E] [MeasurableSpace E] [BorelSpace E]
      [FiniteDimensional Real E], HalfspaceEnlargementFormula (E := E) profile)
    (hGeneral : forall (E : Type u) [NormedAddCommGroup E]
      [InnerProductSpace Real E] [MeasurableSpace E] [BorelSpace E]
      [FiniteDimensional Real E], GeneralSetEnlargementBound (E := E) profile) :
    GaussianIsoperimetricTarget.{u} := by
  intro E _ _ _ _ _ A H hA hH hMeasure r hr
  rw [hHalfspace E H hH r hr, <- hMeasure]
  exact hGeneral E A hA r hr

end Stage1Instances.THM_M_0996

#print axioms Stage1Instances.THM_M_0996.target_of_profile_bounds
