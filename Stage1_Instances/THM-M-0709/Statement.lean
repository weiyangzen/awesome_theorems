import Mathlib.Computability.Halting

/-!
The exact statement surface for undecidability of Post's correspondence problem.
Instances use a fixed binary alphabet and a structured `Primcodable` input type,
so there is no malformed-code case hidden outside the target.
-/

namespace Stage1Instances.THM_M_0709

/-- A finite ordered PCP instance over the fixed binary alphabet. -/
abbrev PCPInstance := List (List Bool × List Bool)

/-- Concatenation of the selected upper words. -/
def upperWord (tiles : PCPInstance) (indices : List (Fin tiles.length)) : List Bool :=
  indices.flatMap fun i => (tiles.get i).1

/-- Concatenation of the selected lower words. -/
def lowerWord (tiles : PCPInstance) (indices : List (Fin tiles.length)) : List Bool :=
  indices.flatMap fun i => (tiles.get i).2

/-- A PCP solution uses one nonempty index sequence on both sides. -/
def IsSolution (tiles : PCPInstance) (indices : List (Fin tiles.length)) : Prop :=
  indices ≠ [] ∧ upperWord tiles indices = lowerWord tiles indices

/-- Semantic solvability of a finite binary PCP instance. -/
def HasSolution (tiles : PCPInstance) : Prop :=
  ∃ indices : List (Fin tiles.length), IsSolution tiles indices

/-- Canonical rev-5.6 target: binary PCP solvability is not a computable predicate. -/
def PostCorrespondenceUndecidable : Prop :=
  ¬ ComputablePred HasSolution

/-- An explicit expansion checks the selected binder and negation scope. -/
theorem postCorrespondenceUndecidable_iff_expanded :
    PostCorrespondenceUndecidable ↔
      ¬ ComputablePred (fun tiles : PCPInstance =>
        ∃ indices : List (Fin tiles.length),
          indices ≠ [] ∧
            indices.flatMap (fun i => (tiles.get i).1) =
              indices.flatMap (fun i => (tiles.get i).2)) := by
  rfl

-- Structural mutations used by the statement validator.
def mutationAllowsEmptyWitness : Prop :=
  ¬ ComputablePred (fun tiles : PCPInstance =>
    ∃ indices : List (Fin tiles.length), upperWord tiles indices = lowerWord tiles indices)

def mutationUnaryAlphabet : Prop :=
  ¬ ComputablePred (fun tiles : List (List Unit × List Unit) =>
    ∃ indices : List (Fin tiles.length),
      indices ≠ [] ∧
        indices.flatMap (fun i => (tiles.get i).1) =
          indices.flatMap (fun i => (tiles.get i).2))

def mutationBoundedWitness : Prop :=
  ¬ ComputablePred (fun tiles : PCPInstance =>
    ∃ indices : List (Fin tiles.length),
      indices ≠ [] ∧ indices.length ≤ tiles.length ∧
        upperWord tiles indices = lowerWord tiles indices)

def mutationDifferentIndexSequences : Prop :=
  ¬ ComputablePred (fun tiles : PCPInstance =>
    ∃ upperIndices lowerIndices : List (Fin tiles.length),
      upperIndices ≠ [] ∧ lowerIndices ≠ [] ∧
        upperWord tiles upperIndices = lowerWord tiles lowerIndices)

/-- With no tiles, a nonempty valid index sequence cannot exist. -/
theorem emptyInstance_hasNoSolution : ¬ HasSolution [] := by
  rintro ⟨indices, hne, -⟩
  cases indices with
  | nil => exact hne rfl
  | cons i _ => exact Fin.elim0 i

#check PostCorrespondenceUndecidable
#print Stage1Instances.THM_M_0709.PostCorrespondenceUndecidable

end Stage1Instances.THM_M_0709
