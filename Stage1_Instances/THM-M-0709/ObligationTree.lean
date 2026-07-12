import Mathlib.Computability.Halting

/-!
This module checks only the exact root interface selected by the frozen obligation
architecture. It deliberately assumes the root and returns it unchanged; no PCP
undecidability proof or composition credit follows from this declaration.
-/

namespace Stage1Instances.THM_M_0709

-- The exact frozen definitions are repeated because this dossier is outside the Lake source tree.
abbrev PCPInstance := List (List Bool × List Bool)

def upperWord (tiles : PCPInstance) (indices : List (Fin tiles.length)) : List Bool :=
  indices.flatMap fun i => (tiles.get i).1

def lowerWord (tiles : PCPInstance) (indices : List (Fin tiles.length)) : List Bool :=
  indices.flatMap fun i => (tiles.get i).2

def IsSolution (tiles : PCPInstance) (indices : List (Fin tiles.length)) : Prop :=
  indices ≠ [] ∧ upperWord tiles indices = lowerWord tiles indices

def HasSolution (tiles : PCPInstance) : Prop :=
  ∃ indices : List (Fin tiles.length), IsSolution tiles indices

def PostCorrespondenceUndecidable : Prop :=
  ¬ ComputablePred HasSolution

/-- Exact-root identity harness. The substantive reduction obligations remain open. -/
theorem root_interface
    (root : PostCorrespondenceUndecidable) :
    PostCorrespondenceUndecidable := by
  exact root

#check root_interface
#print axioms root_interface

end Stage1Instances.THM_M_0709
