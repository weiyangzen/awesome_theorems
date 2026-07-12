import Mathlib.Topology.CWComplex.Classical.Basic
import Mathlib.Topology.Homotopy.Equiv
import Mathlib.Topology.Homotopy.HomotopyGroup

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

-- These definitions are kept definitionally identical to the frozen statement. The standalone
-- worker harness cannot import a module outside the Lake source tree by its repository path.
def zerothHomotopyMap (f : C(X, Y)) : ZerothHomotopy X -> ZerothHomotopy Y :=
  Quotient.map f fun _ _ h => Nonempty.map (fun p => p.map f.continuous) h

def genLoopMap (f : C(X, Y)) (n : Nat) (x : X) :
    GenLoop (Fin n) X x -> GenLoop (Fin n) Y (f x) := fun p =>
  ⟨f.comp p.1, fun y hy => congrArg f (p.2 y hy)⟩

def homotopyGroupMap (f : C(X, Y)) (n : Nat) (x : X) :
    HomotopyGroup.Pi n X x -> HomotopyGroup.Pi n Y (f x) :=
  Quotient.map (genLoopMap f n x) fun _ _ h => h.comp_continuousMap f

def IsWeakHomotopyEquivalence (f : C(X, Y)) : Prop :=
  Function.Bijective (zerothHomotopyMap f) ∧
    ∀ (x : X) (n : Nat), 1 ≤ n -> Function.Bijective (homotopyGroupMap f n x)

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

#check empty_branch
#print axioms empty_branch

end Stage1Instances.THM_M_0559.Proof
