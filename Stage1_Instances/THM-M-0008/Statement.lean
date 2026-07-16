import Mathlib.CategoryTheory.Monoidal.Tor

/-!
Fail-closed Lean surface for the THM-M-0008 statement phase.

The repository record says only "properties of the Tor functor" and does not select one
mathematical proposition. This file therefore declares no canonical target, theorem, proof body,
or credited transport. It replays only the narrow pinned Tor vocabulary needed to distinguish a
source-identity blocker from a missing-library blocker.
-/

noncomputable section

open CategoryTheory CategoryTheory.Limits CategoryTheory.MonoidalCategory

universe u v

namespace Stage1Instances.THM_M_0008.Statement

variable (C : Type u) [Category.{v} C] [MonoidalCategory C]
  [Abelian C] [MonoidalPreadditive C] [HasProjectiveResolutions C]

#check CategoryTheory.Tor
#check CategoryTheory.Tor'
#check CategoryTheory.isZero_Tor_succ_of_projective
#check CategoryTheory.isZero_Tor'_succ_of_projective

end Stage1Instances.THM_M_0008.Statement
