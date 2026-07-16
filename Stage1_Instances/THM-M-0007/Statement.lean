import Mathlib.CategoryTheory.Abelian.RightDerived
import Mathlib.Algebra.Homology.SpectralSequence.Basic

/-!
# THM-M-0007 statement boundary

This module is the minimal pinned interface probe for the Grothendieck spectral-sequence
statement phase. The repository has not admitted source-exact definitions of convergence,
naturality, or the associated abutment filtration, and the pinned mathlib snapshot has no
corresponding convergence predicate. Consequently this file deliberately declares no canonical
target proposition and no proxy theorem. The abbreviations below check only object expressions
that are common to the unresolved source-faithful formulations.
-/

noncomputable section

open CategoryTheory CategoryTheory.Limits

namespace Stage1Instances.THM_M_0007.StatementBoundary

universe uC vC uD vD uE vE

variable {C : Type uC} [Category.{vC} C] [Abelian C] [HasInjectiveResolutions C]
variable {D : Type uD} [Category.{vD} D] [Abelian D] [HasInjectiveResolutions D]
variable {E : Type uE} [Category.{vE} E] [Abelian E]

/-- The object expected at position `(p,q)` on a future source-selected second page. -/
abbrev ExpectedE2Term (F : Functor C D) (G : Functor D E) [F.Additive] [G.Additive]
    (X : C) (p q : Nat) : E :=
  (G.rightDerived p).obj ((F.rightDerived q).obj X)

/-- The object expected in total degree `n`; this abbreviation asserts no convergence. -/
abbrev ExpectedAbutment (F : Functor C D) (G : Functor D E) [F.Additive] [G.Additive]
    (X : C) (n : Nat) : E :=
  ((F ⋙ G).rightDerived n).obj X

/-- The typed first-quadrant cohomological carrier currently supplied by pinned mathlib. -/
abbrev FirstQuadrantE2Carrier : Type _ :=
  E₂CohomologicalSpectralSequenceNat E

#check ExpectedE2Term
#check ExpectedAbutment
#check FirstQuadrantE2Carrier
#check SpectralSequence.page

end Stage1Instances.THM_M_0007.StatementBoundary
