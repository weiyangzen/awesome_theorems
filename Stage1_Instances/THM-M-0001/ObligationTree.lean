import Mathlib.Algebra.Homology.HomologySequence

/-!
# THM-M-0001 conditional obligation composition

The three exactness families are explicit premises.  This file checks their
composition into the continuing long-exact-sequence target; it does not close
those premises or claim the theorem.
-/

universe v u w

namespace Stage1Instances.THM_M_0001.ObligationTree

open CategoryTheory CategoryTheory.Limits HomologicalComplex

variable (C : Type u) [Category.{v} C] [Abelian C]
variable (ι : Type w) (c : ComplexShape ι)
variable (S : ShortComplex (HomologicalComplex C c)) (hS : S.ShortExact)

def SameDegree : Prop :=
  ∀ i : ι,
    (ShortComplex.mk
      (HomologicalComplex.homologyMap S.f i)
      (HomologicalComplex.homologyMap S.g i)
      (by
        rw [← HomologicalComplex.homologyMap_comp, S.zero,
          HomologicalComplex.homologyMap_zero])).Exact

def RightOfG : Prop :=
  ∀ (i j : ι) (hij : c.Rel i j),
    (ShortComplex.mk
      (HomologicalComplex.homologyMap S.g i)
      (hS.δ i j hij)
      (hS.comp_δ i j hij)).Exact

def LeftOfF : Prop :=
  ∀ (i j : ι) (hij : c.Rel i j),
    (ShortComplex.mk
      (hS.δ i j hij)
      (HomologicalComplex.homologyMap S.f j)
      (hS.δ_comp i j hij)).Exact

def Root : Prop :=
  ∀ (C : Type u) [Category.{v} C] [Abelian C]
    (ι : Type w) (c : ComplexShape ι)
    (S : ShortComplex (HomologicalComplex C c)) (hS : S.ShortExact),
    SameDegree C ι c S ∧
      ∀ (i j : ι) (hij : c.Rel i j),
        (ShortComplex.mk
          (HomologicalComplex.homologyMap S.g i)
          (hS.δ i j hij)
          (hS.comp_δ i j hij)).Exact ∧
        (ShortComplex.mk
          (hS.δ i j hij)
          (HomologicalComplex.homologyMap S.f j)
          (hS.δ_comp i j hij)).Exact

/-- Exact child-to-root composition.  Each of the three family premises is
consumed, and no exactness theorem is invoked here. -/
theorem root_compose
    (same : ∀ (C : Type u) [Category.{v} C] [Abelian C]
      (ι : Type w) (c : ComplexShape ι)
      (S : ShortComplex (HomologicalComplex C c)) (_hS : S.ShortExact),
      SameDegree C ι c S)
    (right : ∀ (C : Type u) [Category.{v} C] [Abelian C]
      (ι : Type w) (c : ComplexShape ι)
      (S : ShortComplex (HomologicalComplex C c)) (hS : S.ShortExact),
      RightOfG C ι c S hS)
    (left : ∀ (C : Type u) [Category.{v} C] [Abelian C]
      (ι : Type w) (c : ComplexShape ι)
      (S : ShortComplex (HomologicalComplex C c)) (hS : S.ShortExact),
      LeftOfF C ι c S hS) : Root.{v, u, w} := by
  intro C _ _ ι c S hS
  refine ⟨same C ι c S hS, ?_⟩
  intro i j hij
  exact ⟨right C ι c S hS i j hij, left C ι c S hS i j hij⟩

#check CategoryTheory.ShortComplex.ShortExact.homology_exact₁
#check CategoryTheory.ShortComplex.ShortExact.homology_exact₂
#check CategoryTheory.ShortComplex.ShortExact.homology_exact₃
#print axioms root_compose

end Stage1Instances.THM_M_0001.ObligationTree
