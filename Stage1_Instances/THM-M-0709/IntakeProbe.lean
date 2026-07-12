import Mathlib.Computability.Halting

namespace Stage1Instances.THM_M_0709.IntakeProbe

/-- A direct semantic PCP instance representation used only to probe the intended statement API. -/
abbrev Instance (alphabet : Type) := List (List alphabet × List alphabet)

/-- The same nonempty index sequence makes the upper and lower concatenations agree. -/
def IsMatch {alphabet : Type} (tiles : Instance alphabet)
    (indices : List (Fin tiles.length)) : Prop :=
  indices ≠ [] ∧
    indices.flatMap (fun i => (tiles.get i).1) =
      indices.flatMap (fun i => (tiles.get i).2)

def HasSolution {alphabet : Type} (tiles : Instance alphabet) : Prop :=
  ∃ indices, IsMatch tiles indices

#check ComputablePred
#check IsMatch
#check HasSolution

end Stage1Instances.THM_M_0709.IntakeProbe

