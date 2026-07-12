import Mathlib.Topology.CWComplex.Classical.Basic
import Mathlib.Topology.Homotopy.Equiv
import Mathlib.Topology.Homotopy.HomotopyGroup

/-!
# THM-M-0559: exact Whitehead theorem statement

This module freezes the statement boundary only. It defines the maps induced on path
components and based homotopy groups, then states Whitehead's theorem for whole-space
CW complexes. It does not prove that theorem.
-/

noncomputable section

open scoped Topology Topology.Homotopy

namespace Stage1Instances.THM_M_0559

universe u v

variable {X : Type u} {Y : Type v} [TopologicalSpace X] [TopologicalSpace Y]

/-- The map on path components induced by a continuous map. -/
def zerothHomotopyMap (f : C(X, Y)) : ZerothHomotopy X -> ZerothHomotopy Y :=
  Quotient.map f fun _ _ h => Nonempty.map (fun p => p.map f.continuous) h

/-- Postcomposition sends a generalized loop based at `x` to one based at `f x`. -/
def genLoopMap (f : C(X, Y)) (n : Nat) (x : X) :
    GenLoop (Fin n) X x -> GenLoop (Fin n) Y (f x) := fun p =>
  ⟨f.comp p.1, fun y hy => congrArg f (p.2 y hy)⟩

/-- The function on the `n`th based homotopy groups induced by a continuous map. -/
def homotopyGroupMap (f : C(X, Y)) (n : Nat) (x : X) :
    HomotopyGroup.Pi n X x -> HomotopyGroup.Pi n Y (f x) :=
  Quotient.map (genLoopMap f n x) fun _ _ h =>
    h.comp_continuousMap f

/-- A continuous map is a weak homotopy equivalence in the unbased, possibly disconnected sense. -/
def IsWeakHomotopyEquivalence (f : C(X, Y)) : Prop :=
  Function.Bijective (zerothHomotopyMap f) ∧
    ∀ (x : X) (n : Nat), 1 ≤ n -> Function.Bijective (homotopyGroupMap f n x)

/-- The exact Whitehead target: a weak homotopy equivalence between CW complexes is the
forward map of a homotopy equivalence. -/
def WhiteheadTarget : Prop :=
  ∀ (X : Type u) (Y : Type v) [TopologicalSpace X] [TopologicalSpace Y]
    [Topology.CWComplex (Set.univ : Set X)] [Topology.CWComplex (Set.univ : Set Y)]
    (f : C(X, Y)),
      IsWeakHomotopyEquivalence f ->
        ∃ e : ContinuousMap.HomotopyEquiv X Y, e.toFun = f

/-- Direct expansion of the frozen human claim, retained as a checked alternate encoding. -/
def ExpandedSourceShape : Prop :=
  ∀ (X : Type u) (Y : Type v) [TopologicalSpace X] [TopologicalSpace Y]
    [Topology.CWComplex (Set.univ : Set X)] [Topology.CWComplex (Set.univ : Set Y)]
    (f : C(X, Y)),
      (Function.Bijective (zerothHomotopyMap f) ∧
        ∀ (x : X) (n : Nat), 1 ≤ n -> Function.Bijective (homotopyGroupMap f n x)) ->
          ∃ e : ContinuousMap.HomotopyEquiv X Y, e.toFun = f

/-- The named weak-equivalence predicate is definitionally faithful to the expanded claim. -/
theorem whiteheadTarget_iff_expandedSourceShape :
    WhiteheadTarget.{u, v} ↔ ExpandedSourceShape.{u, v} :=
  Iff.rfl

-- Separately elaborated mutations guard the statement boundary; none is the canonical target.
def mutationRemovedComponents : Prop :=
  ∀ (X : Type u) (Y : Type v) [TopologicalSpace X] [TopologicalSpace Y]
    [Topology.CWComplex (Set.univ : Set X)] [Topology.CWComplex (Set.univ : Set Y)]
    (f : C(X, Y)),
      (∀ (x : X) (n : Nat), 1 ≤ n -> Function.Bijective (homotopyGroupMap f n x)) ->
        ∃ e : ContinuousMap.HomotopyEquiv X Y, e.toFun = f

def mutationAllowsDimensionZero : Prop :=
  ∀ (X : Type u) (Y : Type v) [TopologicalSpace X] [TopologicalSpace Y]
    [Topology.CWComplex (Set.univ : Set X)] [Topology.CWComplex (Set.univ : Set Y)]
    (f : C(X, Y)),
      Function.Bijective (zerothHomotopyMap f) ->
      (∀ (x : X) (n : Nat), Function.Bijective (homotopyGroupMap f n x)) ->
        ∃ e : ContinuousMap.HomotopyEquiv X Y, e.toFun = f

def mutationUnrelatedEquivalence : Prop :=
  ∀ (X : Type u) (Y : Type v) [TopologicalSpace X] [TopologicalSpace Y]
    [Topology.CWComplex (Set.univ : Set X)] [Topology.CWComplex (Set.univ : Set Y)]
    (f : C(X, Y)),
      IsWeakHomotopyEquivalence f -> Nonempty (ContinuousMap.HomotopyEquiv X Y)

end Stage1Instances.THM_M_0559

set_option pp.explicit true in
#print Stage1Instances.THM_M_0559.WhiteheadTarget
