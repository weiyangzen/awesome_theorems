import Mathlib.CategoryTheory.Monoidal.Tor

/-!
This file only checks the pinned Lean vocabulary for one possible interpretation of the
underspecified source phrase "properties of the Tor functor". It is not the canonical target for
THM-M-0008: the repository source does not select projective vanishing over the other incompatible
Tor theorem families recorded in `scope-map.md`.
-/

noncomputable section

open CategoryTheory CategoryTheory.Limits CategoryTheory.MonoidalCategory

universe u v

namespace Stage1Instances.THM_M_0008.StatementCandidateProbe

variable (C : Type u) [Category.{v} C] [MonoidalCategory C]
  [Abelian C] [MonoidalPreadditive C] [HasProjectiveResolutions C]

#check CategoryTheory.Tor
#check CategoryTheory.Tor'
#check CategoryTheory.isZero_Tor_succ_of_projective

variable (X Y : C) [Projective Y] (n : Nat)

#check (show IsZero ((((CategoryTheory.Tor C (n + 1)).obj X).obj Y)) from
  CategoryTheory.isZero_Tor_succ_of_projective C X Y n)

end Stage1Instances.THM_M_0008.StatementCandidateProbe
