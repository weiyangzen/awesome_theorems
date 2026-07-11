import Mathlib.CategoryTheory.Monad.Monadicity

/-!
# THM-M-0085 anchor probes

This module checks the exact pinned mathlib constructor and its terminal
comparison-equivalence field. It inventories a proof candidate; the later
proof phase owns the canonical repository theorem.
-/

noncomputable section

open CategoryTheory

universe v uC uD

namespace Stage1.THM_M_0085.AnchorAudit

variable {C : Type uC} {D : Type uD}
variable [Category.{v} C] [Category.{v} D]
variable {F : CategoryTheory.Functor C D} {G : CategoryTheory.Functor D C}

#check CategoryTheory.Monad.CreatesColimitOfIsSplitPair
#check CategoryTheory.Monad.monadicOfCreatesGSplitCoequalizers
#check CategoryTheory.MonadicRightAdjoint.eqv

/-- Exact-type probe for the projection from mathlib's Beck constructor. -/
example (adj : F ⊣ G) [CategoryTheory.Monad.CreatesColimitOfIsSplitPair G] :
    (CategoryTheory.Monad.comparison adj).IsEquivalence :=
  (CategoryTheory.Monad.monadicOfCreatesGSplitCoequalizers adj).eqv

set_option pp.universes true in
#check CategoryTheory.Monad.monadicOfCreatesGSplitCoequalizers

#print axioms CategoryTheory.Monad.monadicOfCreatesGSplitCoequalizers

end Stage1.THM_M_0085.AnchorAudit
