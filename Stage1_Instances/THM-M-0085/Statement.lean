import Mathlib.CategoryTheory.Monad.Monadicity

/-!
# THM-M-0085: Beck's monadicity theorem statement

This file freezes the creates-`G`-split-coequalizers form of Beck's theorem. It
defines and elaborates the proposition; it does not assert or prove it.
-/

noncomputable section

open CategoryTheory

universe v uC uD

namespace Stage1.THM_M_0085

variable {C : Type uC} {D : Type uD}
variable [Category.{v} C] [Category.{v} D]
variable {F : C ⥤ D} {G : D ⥤ C}

/--
The exact creates-coequalizers form of Beck's monadicity theorem for a fixed
adjunction. The conclusion says that its Eilenberg-Moore comparison functor is
an equivalence, rather than merely choosing some possibly different left
adjoint for `G`.
-/
def StatementShape (adj : F ⊣ G) : Prop :=
  CategoryTheory.Monad.CreatesColimitOfIsSplitPair G →
    (CategoryTheory.Monad.comparison adj).IsEquivalence

/-- The closed target, with universes, categories, functors, and adjunction explicit. -/
def Statement : Prop :=
  ∀ (C : Type uC) (D : Type uD)
      [Category.{v} C] [Category.{v} D]
      (F : C ⥤ D) (G : D ⥤ C) (adj : F ⊣ G),
    StatementShape adj

/-- Kernel-checked expansion of the canonical target. -/
theorem statement_iff :
    Statement.{v, uC, uD} ↔
      ∀ (C : Type uC) (D : Type uD)
          [Category.{v} C] [Category.{v} D]
          (F : C ⥤ D) (G : D ⥤ C) (adj : F ⊣ G),
        CategoryTheory.Monad.CreatesColimitOfIsSplitPair G →
          (CategoryTheory.Monad.comparison adj).IsEquivalence := by
  rfl

-- Separately elaborated mutations, compared by `check_statement.py`.
def mutationRemovedCreatesHypothesis : Prop :=
  ∀ (C : Type uC) (D : Type uD)
      [Category.{v} C] [Category.{v} D]
      (F : C ⥤ D) (G : D ⥤ C) (adj : F ⊣ G),
    (CategoryTheory.Monad.comparison adj).IsEquivalence

def mutationChangedDomain : Prop :=
  ∀ (C : Type uC) (D : Type uD)
      [Category.{v} C] [Category.{v} D]
      (F : C ⥤ D) (G : D ⥤ C) (adj : F ⊣ G),
    CategoryTheory.Monad.CreatesColimitOfIsSplitPair F →
      (CategoryTheory.Monad.comparison adj).IsEquivalence

def mutationChangedBinderScope : Prop :=
  ∀ (C : Type uC) (D : Type uD)
      [Category.{v} C] [Category.{v} D]
      (F : C ⥤ D) (G : D ⥤ C),
    CategoryTheory.Monad.CreatesColimitOfIsSplitPair G →
      ∀ (adj : F ⊣ G),
        (CategoryTheory.Monad.comparison adj).IsEquivalence

def mutationExcludeEmptyRightCategory : Prop :=
  ∀ (C : Type uC) (D : Type uD)
      [Category.{v} C] [Category.{v} D] [Nonempty D]
      (F : C ⥤ D) (G : D ⥤ C) (adj : F ⊣ G),
    StatementShape adj

#check Statement
#check StatementShape
set_option pp.universes true in
set_option pp.explicit true in
#print Statement

end Stage1.THM_M_0085
