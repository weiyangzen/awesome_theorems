import Mathlib.Topology.CWComplex.Classical.Basic
import Mathlib.Topology.Homotopy.Equiv
import Mathlib.Topology.Homotopy.HomotopyGroup

/-!
# THM-M-0559 conditional composition certificate

This module checks only the final composition boundary of the frozen obligation tree.  The
substantive Whitehead core remains an explicit premise for the later proof phase.
-/

noncomputable section

open scoped Topology Topology.Homotopy

namespace Stage1Instances.THM_M_0559

universe u v

variable {X : Type u} {Y : Type v} [TopologicalSpace X] [TopologicalSpace Y]

-- Standalone copies of the frozen definitions let this narrow harness elaborate without first
-- producing an olean outside Lake's configured source tree. Source hashes bind it to Statement.lean.
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

def WhiteheadTarget : Prop :=
  ∀ (X : Type u) (Y : Type v) [TopologicalSpace X] [TopologicalSpace Y]
    [Topology.CWComplex (Set.univ : Set X)] [Topology.CWComplex (Set.univ : Set Y)]
    (f : C(X, Y)), IsWeakHomotopyEquivalence f ->
      ∃ e : ContinuousMap.HomotopyEquiv X Y, e.toFun = f

def ExpandedSourceShape : Prop :=
  ∀ (X : Type u) (Y : Type v) [TopologicalSpace X] [TopologicalSpace Y]
    [Topology.CWComplex (Set.univ : Set X)] [Topology.CWComplex (Set.univ : Set Y)]
    (f : C(X, Y)),
      (Function.Bijective (zerothHomotopyMap f) ∧
        ∀ (x : X) (n : Nat), 1 ≤ n -> Function.Bijective (homotopyGroupMap f n x)) ->
          ∃ e : ContinuousMap.HomotopyEquiv X Y, e.toFun = f

/-- The direct, componentwise proof obligation, written without hiding the target behind an alias. -/
def DirectWhiteheadCore : Prop :=
  ∀ (X : Type u) (Y : Type v) [TopologicalSpace X] [TopologicalSpace Y]
    [Topology.CWComplex (Set.univ : Set X)] [Topology.CWComplex (Set.univ : Set Y)]
    (f : C(X, Y)),
      (Function.Bijective (zerothHomotopyMap f) ∧
        ∀ (x : X) (n : Nat), 1 ≤ n -> Function.Bijective (homotopyGroupMap f n x)) ->
          ∃ e : ContinuousMap.HomotopyEquiv X Y, e.toFun = f

/-- Checked transport from the open direct core to the exact canonical target. -/
theorem root_of_directWhiteheadCore
    (h : DirectWhiteheadCore.{u, v}) : WhiteheadTarget.{u, v} :=
  h

/-- The conditional composition premise has exactly the expanded frozen source shape. -/
theorem directWhiteheadCore_iff_expandedSourceShape :
    DirectWhiteheadCore.{u, v} ↔ ExpandedSourceShape.{u, v} :=
  Iff.rfl

end Stage1Instances.THM_M_0559

#check Stage1Instances.THM_M_0559.root_of_directWhiteheadCore
#print axioms Stage1Instances.THM_M_0559.root_of_directWhiteheadCore
