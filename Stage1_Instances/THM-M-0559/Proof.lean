import Mathlib.Topology.CWComplex.Classical.Basic
import Mathlib.Topology.Homotopy.Equiv
import Mathlib.Topology.Homotopy.HomotopyGroup
import Stage1_Instances.«THM-M-0559».Statement

/-!
# THM-M-0559 proof work

This module closes the empty-space branch of the frozen Whitehead obligation tree. The central
cellular Whitehead construction is not available in the pinned mathlib revision, so this is not a
proof of `WhiteheadTarget`.
-/

noncomputable section

open scoped Topology Topology.Homotopy

namespace Stage1Instances.THM_M_0559.Proof

universe u v

variable {X : Type u} {Y : Type v} [TopologicalSpace X] [TopologicalSpace Y]

open Stage1Instances.THM_M_0559

/-- An equality of path components produces a path between its chosen representatives. -/
theorem joined_of_component_eq {x x' : X}
    (h : (Quotient.mk (pathSetoid X) x : ZerothHomotopy X) =
      Quotient.mk (pathSetoid X) x') : Joined x x' :=
  Quotient.exact h

/-- Component surjectivity supplies a source point mapping into any chosen target component. -/
theorem exists_preimage_joined (f : C(X, Y))
    (hf : Function.Surjective (zerothHomotopyMap f)) (y : Y) :
    ∃ x : X, Joined (f x) y := by
  obtain ⟨q, hq⟩ := hf (Quotient.mk (pathSetoid Y) y)
  refine Quotient.inductionOn q (fun x hx => ⟨x, ?_⟩) hq
  exact Quotient.exact hx

/-- Component injectivity reflects path-connectedness between source points. -/
theorem joined_of_map_joined (f : C(X, Y))
    (hf : Function.Injective (zerothHomotopyMap f)) {x x' : X}
    (h : Joined (f x) (f x')) : Joined x x' := by
  change (pathSetoid X).r x x'
  apply Quotient.exact
  apply hf
  exact Quotient.sound h

/-- Component surjectivity is representativewise coverage up to a path. -/
theorem components_surjective_iff (f : C(X, Y)) :
    Function.Surjective (zerothHomotopyMap f) ↔
      ∀ y : Y, ∃ x : X, Joined (f x) y := by
  constructor
  · intro hf y
    exact exists_preimage_joined f hf y
  · intro hf q
    refine Quotient.inductionOn q (fun y => ?_)
    obtain ⟨x, hx⟩ := hf y
    exact ⟨Quotient.mk (pathSetoid X) x, Quotient.sound hx⟩

/-- Component injectivity is reflection of paths between image points. -/
theorem components_injective_iff (f : C(X, Y)) :
    Function.Injective (zerothHomotopyMap f) ↔
      ∀ x x' : X, Joined (f x) (f x') → Joined x x' := by
  constructor
  · intro hf x x' h
    exact joined_of_map_joined f hf h
  · intro hf q q'
    refine Quotient.inductionOn₂ q q' (fun x x' h => ?_)
    exact Quotient.sound (hf x x' (Quotient.exact h))

/-- Component bijectivity supplies both componentwise coverage and reflection. -/
theorem components_bijective_iff (f : C(X, Y)) :
    Function.Bijective (zerothHomotopyMap f) ↔
      (∀ y : Y, ∃ x : X, Joined (f x) y) ∧
        ∀ x x' : X, Joined (f x) (f x') → Joined x x' := by
  change (Function.Injective (zerothHomotopyMap f) ∧
    Function.Surjective (zerothHomotopyMap f)) ↔ _
  rw [components_surjective_iff, components_injective_iff, and_comm]

/-- Path components are inhabited exactly when their underlying space is inhabited. -/
theorem nonempty_zerothHomotopy_iff : Nonempty (ZerothHomotopy X) ↔ Nonempty X := by
  constructor
  · rintro ⟨q⟩
    exact Quotient.inductionOn q fun x => ⟨x⟩
  · rintro ⟨x⟩
    exact ⟨Quotient.mk (pathSetoid X) x⟩

/-- A bijection on path components detects the empty-space boundary in both directions. -/
theorem nonempty_iff_of_components_bijective (f : C(X, Y))
    (hf : Function.Bijective (zerothHomotopyMap f)) : Nonempty X ↔ Nonempty Y := by
  constructor
  · rintro hX
    have h0X : Nonempty (ZerothHomotopy X) := nonempty_zerothHomotopy_iff.mpr hX
    obtain ⟨x0⟩ := h0X
    exact nonempty_zerothHomotopy_iff.mp ⟨zerothHomotopyMap f x0⟩
  · rintro hY
    have h0Y : Nonempty (ZerothHomotopy Y) := nonempty_zerothHomotopy_iff.mpr hY
    obtain ⟨y0⟩ := h0Y
    obtain ⟨x0, _⟩ := hf.2 y0
    exact nonempty_zerothHomotopy_iff.mp ⟨x0⟩

/-- The exact `M0559-B-EMPTY` branch: when the source is empty, component bijectivity forces the
target to be empty and the prescribed map is the forward map of a homotopy equivalence. -/
theorem empty_branch (f : C(X, Y)) (hf : IsWeakHomotopyEquivalence f) [IsEmpty X] :
    ∃ e : ContinuousMap.HomotopyEquiv X Y, e.toFun = f := by
  have hy : ¬ Nonempty Y := by
    intro hY
    exact not_nonempty_iff.mpr inferInstance ((nonempty_iff_of_components_bijective f hf.1).mpr hY)
  letI : IsEmpty Y := not_nonempty_iff.mp hy
  let h : X ≃ₜ Y :=
    { toEquiv :=
        { toFun := fun x => isEmptyElim x
          invFun := fun y => isEmptyElim y
          left_inv := fun x => isEmptyElim x
          right_inv := fun y => isEmptyElim y }
      continuous_toFun := continuous_def.mpr fun _ _ => by
        convert isOpen_empty
        ext x
        exact isEmptyElim x
      continuous_invFun := continuous_def.mpr fun _ _ => by
        convert isOpen_empty
        ext y
        exact isEmptyElim y }
  refine ⟨h.toHomotopyEquiv, ?_⟩
  ext x
  exact isEmptyElim x

#print axioms joined_of_component_eq
#print axioms exists_preimage_joined
#print axioms joined_of_map_joined
#print axioms components_surjective_iff
#print axioms components_injective_iff
#print axioms components_bijective_iff
#print axioms nonempty_zerothHomotopy_iff
#print axioms nonempty_iff_of_components_bijective
#print axioms empty_branch
#print sorries joined_of_component_eq
#print sorries exists_preimage_joined
#print sorries joined_of_map_joined
#print sorries components_surjective_iff
#print sorries components_injective_iff
#print sorries components_bijective_iff
#print sorries nonempty_zerothHomotopy_iff
#print sorries nonempty_iff_of_components_bijective
#print sorries empty_branch

end Stage1Instances.THM_M_0559.Proof
