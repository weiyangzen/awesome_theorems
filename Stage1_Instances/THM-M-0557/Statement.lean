import Mathlib.Topology.Homotopy.HomotopyGroup

/-!
# THM-M-0557: exact homotopy-group structure statement

This module freezes and tests the statement boundary only. It does not claim
the downstream proof, source, or release gates.
-/

namespace Stage1Instances.THM_M_0557

universe u

/-- For every pointed topological space, the positive-dimensional homotopy
groups carry group structures and the groups in dimensions at least two carry
commutative group structures. The offsets make the two dimension boundaries
part of the expression. -/
def HomotopyGroupStructureTarget : Prop :=
  forall (X : Type u) [TopologicalSpace X] (x : X) (n : Nat),
    Nonempty (Group (HomotopyGroup.Pi (n + 1) X x)) /\
      Nonempty (CommGroup (HomotopyGroup.Pi (n + 2) X x))

-- Separately elaborated structural mutations used by `check_statement.py`.
def mutationIncludesDimensionZero : Prop :=
  forall (X : Type u) [TopologicalSpace X] (x : X) (n : Nat),
    Nonempty (Group (HomotopyGroup.Pi n X x)) /\
      Nonempty (CommGroup (HomotopyGroup.Pi (n + 2) X x))

def mutationCommutativeFromDimensionOne : Prop :=
  forall (X : Type u) [TopologicalSpace X] (x : X) (n : Nat),
    Nonempty (Group (HomotopyGroup.Pi (n + 1) X x)) /\
      Nonempty (CommGroup (HomotopyGroup.Pi (n + 1) X x))

def mutationFixedDimensionTwo : Prop :=
  forall (X : Type u) [TopologicalSpace X] (x : X),
    Nonempty (Group (HomotopyGroup.Pi 2 X x)) /\
      Nonempty (CommGroup (HomotopyGroup.Pi 2 X x))

def mutationUnpointedExistentialBasepoint : Prop :=
  forall (X : Type u) [TopologicalSpace X], exists x : X, forall n : Nat,
    Nonempty (Group (HomotopyGroup.Pi (n + 1) X x)) /\
      Nonempty (CommGroup (HomotopyGroup.Pi (n + 2) X x))

-- Boundary witnesses check the intended pinned API at dimensions one and two.
example (X : Type u) [TopologicalSpace X] (x : X) :
    Nonempty (Group (HomotopyGroup.Pi 1 X x)) := by
  exact ⟨inferInstance⟩

example (X : Type u) [TopologicalSpace X] (x : X) :
    Nonempty (CommGroup (HomotopyGroup.Pi 2 X x)) := by
  exact ⟨inferInstance⟩

end Stage1Instances.THM_M_0557

set_option pp.explicit true in
#print Stage1Instances.THM_M_0557.HomotopyGroupStructureTarget
