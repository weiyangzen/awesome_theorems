import «Stage1_Instances».«THM-M-0996».ObligationTree
import Mathlib.Util.AssertNoSorry

/-!
# THM-M-0996 validation probes

This module independently reconstructs one elementary half-space boundary and
the conditional child-to-root composition. It deliberately does not import
`Proof`: the arbitrary-set Gaussian enlargement bound remains an explicit
premise, so no premise-free proof of the canonical root is asserted.
-/

noncomputable section

open MeasureTheory ProbabilityTheory

namespace Stage1Instances.THM_M_0996.Validation

open Stage1Instances.THM_M_0996

universe u

/-- Independent reconstruction of measurability for a frozen closed affine
half-space. This checks only an elementary support boundary. -/
theorem measurableSet_of_isUnitHalfspace_direct
    {E : Type u} [NormedAddCommGroup E] [NormedSpace Real E]
    [MeasurableSpace E] [BorelSpace E] {H : Set E}
    (hH : IsUnitHalfspace H) : MeasurableSet H := by
  obtain ⟨L, c, _, rfl⟩ := hH
  exact isClosed_Iic.preimage L.continuous |>.measurableSet

/-- Independent reconstruction of the frozen conditional composition. The
`hGeneral` argument is exactly the still-open arbitrary-set theorem. -/
theorem conditionalTargetDirect
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

#print sorries measurableSet_of_isUnitHalfspace_direct
#print axioms measurableSet_of_isUnitHalfspace_direct
#print sorries conditionalTargetDirect
#print axioms conditionalTargetDirect

end Stage1Instances.THM_M_0996.Validation
