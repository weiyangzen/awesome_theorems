import Mathlib.CategoryTheory.Monad.Monadicity

/-!
# THM-M-0085 obligation composition probe

This file checks the two semantic proof steps selected by the frozen
architecture: install the proposition-valued creates hypothesis as the local
instance expected by mathlib, then project the fixed-adjunction comparison
equivalence from the pinned Beck constructor.  The proof phase still owns the
named canonical repository theorem.
-/

noncomputable section

open CategoryTheory

universe v uC uD

namespace Stage1.THM_M_0085.ObligationTree

variable {C : Type uC} {D : Type uD}
variable [Category.{v} C] [Category.{v} D]
variable {F : C ⥤ D} {G : D ⥤ C}

/-- Checked child-to-parent composition for the frozen proof route. -/
example (adj : F ⊣ G)
    (creates : CategoryTheory.Monad.CreatesColimitOfIsSplitPair G) :
    (CategoryTheory.Monad.comparison adj).IsEquivalence := by
  letI : CategoryTheory.Monad.CreatesColimitOfIsSplitPair G := creates
  exact (CategoryTheory.Monad.monadicOfCreatesGSplitCoequalizers adj).eqv

#print axioms CategoryTheory.Monad.monadicOfCreatesGSplitCoequalizers

end Stage1.THM_M_0085.ObligationTree
