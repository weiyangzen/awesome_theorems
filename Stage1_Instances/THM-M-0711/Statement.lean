import Mathlib.Computability.Halting
import Mathlib.GroupTheory.PresentedGroup

namespace Stage1.THM_M_0711

/-- Evaluate an effective list encoding of signed generators in the free group. -/
def evalWord {n : ℕ} (word : List (Fin n × Bool)) : FreeGroup (Fin n) :=
  (word.map fun (i, inverse) =>
    if inverse then (FreeGroup.of i)⁻¹ else FreeGroup.of i).prod

/-- The fixed-presentation form of the Novikov-Boone theorem: some group with a
finite presentation has a noncomputable identity problem on freely reduced words. -/
def NovikovBooneTarget : Prop :=
  ∃ (n : ℕ) (rels : Finset (FreeGroup (Fin n))),
    ¬ComputablePred fun word : List (Fin n × Bool) =>
      PresentedGroup.mk (rels : Set (FreeGroup (Fin n))) (evalWord word) = 1

#check NovikovBooneTarget

-- Structural mutations must not be definitionally identical to the frozen target.
#check_failure (rfl : NovikovBooneTarget =
  ∀ (n : ℕ) (rels : Finset (FreeGroup (Fin n))),
    ¬ComputablePred fun word : List (Fin n × Bool) =>
      PresentedGroup.mk (rels : Set (FreeGroup (Fin n))) (evalWord word) = 1)

#check_failure (rfl : NovikovBooneTarget =
  ∃ (n : ℕ) (rels : Finset (FreeGroup (Fin n))),
    ComputablePred fun word : List (Fin n × Bool) =>
      PresentedGroup.mk (rels : Set (FreeGroup (Fin n))) (evalWord word) = 1)

#check_failure (rfl : NovikovBooneTarget =
  ∃ rels : Finset (FreeGroup (Fin 0)),
    ¬ComputablePred fun word : List (Fin 0 × Bool) =>
      PresentedGroup.mk (rels : Set (FreeGroup (Fin 0))) (evalWord word) = 1)

set_option pp.explicit true in
set_option pp.universes true in
#print NovikovBooneTarget

end Stage1.THM_M_0711
