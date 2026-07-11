import Mathlib.NumberTheory.NumberField.ClassNumber

/-!
# THM-M-0418: Minkowski bound for ideal classes

This module freezes and elaborates the representative form of the Minkowski
bound. It contains statement-level transports and mutation fixtures, but does
not claim a new proof of the bound.
-/

open scoped nonZeroDivisors Real

open Module NumberField Ideal Nat

namespace Stage1Instances.THM_M_0418

universe u

/-- The explicit real-valued Minkowski constant used in mathlib's class-number theorem. -/
noncomputable def MinkowskiClassBound
    (K : Type u) [Field K] [NumberField K] : Real :=
  (4 / Real.pi) ^ NumberField.InfinitePlace.nrComplexPlaces K *
    ((finrank ℚ K).factorial / (finrank ℚ K) ^ (finrank ℚ K) *
      Real.sqrt |NumberField.discr K|)

/-- The exact representative-form target selected by the rev-5.6 intake. -/
def MinkowskiIdealClassBound : Prop :=
  ∀ (K : Type u) [Field K] [NumberField K]
    (C : ClassGroup (RingOfIntegers K)),
      ∃ I : (Ideal (RingOfIntegers K))⁰,
        ClassGroup.mk0 I = C ∧
          absNorm (I : Ideal (RingOfIntegers K)) ≤ MinkowskiClassBound K

/-- Direct local spelling of the pinned mathlib declaration's proposition. -/
def PinnedMathlibSourceShape : Prop :=
  ∀ (K : Type u) [Field K] [NumberField K]
    (C : ClassGroup (RingOfIntegers K)),
      ∃ I : (Ideal (RingOfIntegers K))⁰,
        ClassGroup.mk0 I = C ∧
          absNorm (I : Ideal (RingOfIntegers K)) ≤
            (4 / Real.pi) ^ NumberField.InfinitePlace.nrComplexPlaces K *
              ((finrank ℚ K).factorial / (finrank ℚ K) ^ (finrank ℚ K) *
                Real.sqrt |NumberField.discr K|)

/-- Checked statement transport to the literal type of the pinned mathlib anchor. -/
theorem minkowskiIdealClassBound_iff_pinnedMathlibSourceShape :
    MinkowskiIdealClassBound.{u} ↔ PinnedMathlibSourceShape.{u} := by
  rfl

-- Separately elaborated structural mutations. They receive no equivalence or proof credit.
def MutationChangedClassOrientation : Prop :=
  ∀ (K : Type u) [Field K] [NumberField K]
    (C : ClassGroup (RingOfIntegers K)),
      ∃ I : (Ideal (RingOfIntegers K))⁰,
        ClassGroup.mk0 I = C⁻¹ ∧
          absNorm (I : Ideal (RingOfIntegers K)) ≤ MinkowskiClassBound K

def MutationStrictEndpoint : Prop :=
  ∀ (K : Type u) [Field K] [NumberField K]
    (C : ClassGroup (RingOfIntegers K)),
      ∃ I : (Ideal (RingOfIntegers K))⁰,
        ClassGroup.mk0 I = C ∧
          absNorm (I : Ideal (RingOfIntegers K)) < MinkowskiClassBound K

def MutationRemovedNonzeroIdeal : Prop :=
  ∀ (K : Type u) [Field K] [NumberField K]
    (C : ClassGroup (RingOfIntegers K)),
      ∃ I : Ideal (RingOfIntegers K),
        I ≠ 0 ∧ absNorm I ≤ MinkowskiClassBound K

def MutationChangedBound : Prop :=
  ∀ (K : Type u) [Field K] [NumberField K]
    (C : ClassGroup (RingOfIntegers K)),
      ∃ I : (Ideal (RingOfIntegers K))⁰,
        ClassGroup.mk0 I = C ∧
          absNorm (I : Ideal (RingOfIntegers K)) ≤
            Real.sqrt |NumberField.discr K|

end Stage1Instances.THM_M_0418

#check NumberField.exists_ideal_in_class_of_norm_le

set_option pp.explicit true in
#print Stage1Instances.THM_M_0418.MinkowskiIdealClassBound
