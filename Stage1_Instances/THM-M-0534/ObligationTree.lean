import Statement

/-!
# THM-M-0534 conditional obligation composition

This module checks only that the three exactness-family obligations compose to the frozen root.
The imported homology theorems remain explicit bridge obligations; this file does not close them.
-/

universe v u w

namespace Stage1Instances.THM_M_0534.ObligationTree

open CategoryTheory
open CategoryTheory.Limits
open HomologicalComplex

def SameDegreeFamily : Prop :=
  forall (C : Type u) [Category.{v} C] [Abelian C]
    (iota : Type w) (c : ComplexShape iota)
    (S : ShortComplex (HomologicalComplex C c)) (hS : S.ShortExact) (i : iota),
    (ShortComplex.mk
      (HomologicalComplex.homologyMap S.f i)
      (HomologicalComplex.homologyMap S.g i)
      (by rw [← HomologicalComplex.homologyMap_comp, S.zero,
        HomologicalComplex.homologyMap_zero])).Exact

def IntoDeltaFamily : Prop :=
  forall (C : Type u) [Category.{v} C] [Abelian C]
    (iota : Type w) (c : ComplexShape iota)
    (S : ShortComplex (HomologicalComplex C c)) (hS : S.ShortExact)
    (i j : iota) (hij : c.Rel i j),
    (ShortComplex.mk
      (HomologicalComplex.homologyMap S.g i)
      (hS.δ i j hij)
      (hS.comp_δ i j hij)).Exact

def OutOfDeltaFamily : Prop :=
  forall (C : Type u) [Category.{v} C] [Abelian C]
    (iota : Type w) (c : ComplexShape iota)
    (S : ShortComplex (HomologicalComplex C c)) (hS : S.ShortExact)
    (i j : iota) (hij : c.Rel i j),
    (ShortComplex.mk
      (hS.δ i j hij)
      (HomologicalComplex.homologyMap S.f j)
      (hS.δ_comp i j hij)).Exact

/-- Kernel-checked composition certificate for the root, conditional on all three families. -/
theorem root_of_exactness_families
    (same : SameDegreeFamily.{v, u, w})
    (into : IntoDeltaFamily.{v, u, w})
    (out : OutOfDeltaFamily.{v, u, w}) :
    Stage1Instances.THM_M_0534.LongExactHomologySequenceTarget.{v, u, w} := by
  intro C _ _ iota c S hS
  exact ⟨same C iota c S hS, fun i j hij =>
    ⟨into C iota c S hS i j hij, out C iota c S hS i j hij⟩⟩

#print axioms root_of_exactness_families

end Stage1Instances.THM_M_0534.ObligationTree
