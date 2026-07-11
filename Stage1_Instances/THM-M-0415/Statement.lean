import Mathlib.NumberTheory.NumberField.ClassNumber

/-!
# THM-M-0415: exact ideal-class-group finiteness statement

This module freezes and tests the statement boundary only. It does not claim
rev-5.6 proof, provenance, validation, or release acceptance.
-/

open scoped NumberField

namespace Stage1Instances.THM_M_0415

universe u

/-- The exact target: the ideal class group of the ring of integers of every
number field is finite. -/
def IdealClassGroupFiniteTarget : Prop :=
  ∀ (K : Type u) [Field K] [NumberField K],
    Finite (ClassGroup (NumberField.RingOfIntegers K))

/-- The stronger data-bearing presentation kept separate from the canonical
source-level finiteness proposition. -/
def FintypePresentation : Prop :=
  ∀ (K : Type u) [Field K] [NumberField K],
    Nonempty (Fintype (ClassGroup (NumberField.RingOfIntegers K)))

/-- Checked transport between source-level finiteness and a data-bearing
`Fintype` presentation. -/
theorem idealClassGroupFiniteTarget_iff_fintypePresentation :
    IdealClassGroupFiniteTarget.{u} ↔ FintypePresentation.{u} := by
  constructor
  · intro h K _ _
    haveI : Finite (ClassGroup (NumberField.RingOfIntegers K)) := h K
    exact ⟨Fintype.ofFinite (ClassGroup (NumberField.RingOfIntegers K))⟩
  · intro h K _ _
    letI : Fintype (ClassGroup (NumberField.RingOfIntegers K)) := (h K).some
    exact Finite.of_fintype (ClassGroup (NumberField.RingOfIntegers K))

-- Structural mutations elaborated separately and rejected by the validator.
def mutationRemovedNumberField : Prop :=
  ∀ (K : Type u) [Field K], Finite (ClassGroup K)

def mutationChangedDomainToRat : Prop :=
  Finite (ClassGroup (NumberField.RingOfIntegers ℚ))

def mutationChangedBinderScope : Prop :=
  ∀ (K : Type u) [Field K], NumberField K →
    Finite (ClassGroup (NumberField.RingOfIntegers K))

def mutationBoundaryClassNumberOne : Prop :=
  ∀ (K : Type u) [Field K] [NumberField K],
    NumberField.classNumber K = 1 →
      Finite (ClassGroup (NumberField.RingOfIntegers K))

/-- The rational field boundary is genuinely within the canonical target. -/
theorem rational_boundary :
    Finite (ClassGroup (NumberField.RingOfIntegers ℚ)) := by
  infer_instance

end Stage1Instances.THM_M_0415

set_option pp.explicit true in
#print Stage1Instances.THM_M_0415.IdealClassGroupFiniteTarget
