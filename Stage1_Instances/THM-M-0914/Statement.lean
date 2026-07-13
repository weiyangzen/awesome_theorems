/-!
# THM-M-0914 canonical Lean statement

This module freezes the literal `n + 1` objects into `n` boxes formulation of
the finite pigeonhole principle. It contains statement transports, mutation
fixtures, and boundary checks, but no proof of the canonical target.
-/

namespace Stage1Instances.THM_M_0914

/-- Every total placement of `n + 1` objects into `n` boxes has a collision. -/
def PigeonholeTarget : Prop :=
  ∀ (n : Nat) (f : Fin (n + 1) → Fin n),
    ∃ x y, x ≠ y ∧ f x = f y

/-- The same claim with the shared box named explicitly. -/
def BoxWitnessTarget : Prop :=
  ∀ (n : Nat) (f : Fin (n + 1) → Fin n),
    ∃ b x y, x ≠ y ∧ f x = b ∧ f y = b

/-- Checked transport between equal images and an explicit box witness. -/
theorem pigeonholeTarget_iff_boxWitnessTarget :
    PigeonholeTarget ↔ BoxWitnessTarget := by
  constructor
  · rintro h n f
    obtain ⟨x, y, hxy, heq⟩ := h n f
    exact ⟨f x, x, y, hxy, rfl, heq.symm⟩
  · rintro h n f
    obtain ⟨b, x, y, hxy, hxb, hyb⟩ := h n f
    exact ⟨x, y, hxy, hxb.trans hyb.symm⟩

/-! Structural mutations elaborate but receive no statement-identity credit. -/

/-- Removed-contract mutation: the two object witnesses need not be distinct. -/
def mutationRemovedDistinctness : Prop :=
  ∀ (n : Nat) (f : Fin (n + 1) → Fin n),
    ∃ x y, f x = f y

/-- Domain mutation: use `n + 2` objects rather than the literal `n + 1`. -/
def mutationChangedDomain : Prop :=
  ∀ (n : Nat) (f : Fin (n + 2) → Fin n),
    ∃ x y, x ≠ y ∧ f x = f y

/-- Binder-scope mutation: choose one pair before the placement function. -/
def mutationChangedBinderScope : Prop :=
  ∀ (n : Nat), ∃ x y : Fin (n + 1),
    x ≠ y ∧ ∀ f : Fin (n + 1) → Fin n, f x = f y

/-- Boundary mutation: exclude the zero-box case with a positivity premise. -/
def mutationExcludesZeroBoxes : Prop :=
  ∀ (n : Nat), 0 < n → ∀ f : Fin (n + 1) → Fin n,
    ∃ x y, x ≠ y ∧ f x = f y

variable
  (hRemoved : mutationRemovedDistinctness)
  (hDomain : mutationChangedDomain)
  (hScope : mutationChangedBinderScope)
  (hBoundary : mutationExcludesZeroBoxes)

#check_failure (show PigeonholeTarget from hRemoved)
#check_failure (show PigeonholeTarget from hDomain)
#check_failure (show PigeonholeTarget from hScope)
#check_failure (show PigeonholeTarget from hBoundary)

/-! Boundary witnesses inspect the encoding without proving the root target. -/

/-- At `n = 0`, no total placement from the one-object type exists. -/
theorem no_placement_into_zero_boxes : ¬ Nonempty (Fin 1 → Fin 0) := by
  rintro ⟨f⟩
  exact (f 0).elim0

/-- At `n = 1`, every placement of the two objects has the required collision. -/
theorem one_box_boundary (f : Fin 2 → Fin 1) :
    ∃ x y : Fin 2, x ≠ y ∧ f x = f y := by
  exact ⟨0, 1, by decide, Subsingleton.elim _ _⟩

#print axioms pigeonholeTarget_iff_boxWitnessTarget
#print axioms no_placement_into_zero_boxes
#print axioms one_box_boundary

set_option pp.universes true in
set_option pp.explicit true in
#print PigeonholeTarget

end Stage1Instances.THM_M_0914
