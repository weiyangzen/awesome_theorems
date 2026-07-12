import Mathlib.Algebra.Homology.HomologySequence

/-!
# THM-M-0534: long exact sequence in homology

This module freezes the general chain-complex statement selected from the repository's literal
claim. It states the continuing sequence, rather than only one finite window, and contains no proof
of that target.
-/

universe v u w

namespace Stage1Instances.THM_M_0534

open CategoryTheory
open CategoryTheory.Limits
open HomologicalComplex

/-- Exactness at all three repeating positions in the homology sequence induced by a short exact
sequence of homological complexes. The first conjunct separately covers every degree, including a
degree with no outgoing shape relation. -/
def LongExactHomologySequenceTarget : Prop :=
  ∀ (C : Type u) [Category.{v} C] [Abelian C]
    (ι : Type w) (c : ComplexShape ι)
    (S : ShortComplex (HomologicalComplex C c)) (hS : S.ShortExact),
    (∀ i : ι,
      (ShortComplex.mk
        (HomologicalComplex.homologyMap S.f i)
        (HomologicalComplex.homologyMap S.g i)
        (by
          rw [← HomologicalComplex.homologyMap_comp, S.zero,
            HomologicalComplex.homologyMap_zero])).Exact) ∧
    (∀ (i j : ι) (hij : c.Rel i j),
      (ShortComplex.mk
        (HomologicalComplex.homologyMap S.g i)
        (hS.δ i j hij)
        (hS.comp_δ i j hij)).Exact ∧
      (ShortComplex.mk
        (hS.δ i j hij)
        (HomologicalComplex.homologyMap S.f j)
        (hS.δ_comp i j hij)).Exact)

/-- A logically regrouped encoding of the same three universally quantified exactness families. -/
def GroupedLongExactHomologySequenceTarget : Prop :=
  ∀ (C : Type u) [Category.{v} C] [Abelian C]
    (ι : Type w) (c : ComplexShape ι)
    (S : ShortComplex (HomologicalComplex C c)) (hS : S.ShortExact),
    (∀ i : ι,
      (ShortComplex.mk
        (HomologicalComplex.homologyMap S.f i)
        (HomologicalComplex.homologyMap S.g i)
        (by
          rw [← HomologicalComplex.homologyMap_comp, S.zero,
            HomologicalComplex.homologyMap_zero])).Exact) ∧
    (∀ (i j : ι) (hij : c.Rel i j),
      (ShortComplex.mk
        (HomologicalComplex.homologyMap S.g i)
        (hS.δ i j hij)
        (hS.comp_δ i j hij)).Exact) ∧
    (∀ (i j : ι) (hij : c.Rel i j),
      (ShortComplex.mk
        (hS.δ i j hij)
        (HomologicalComplex.homologyMap S.f j)
        (hS.δ_comp i j hij)).Exact)

/-- Kernel-checked transport between the canonical and grouped encodings. -/
theorem longExactHomologySequenceTarget_iff_grouped :
    LongExactHomologySequenceTarget.{v, u, w} ↔
      GroupedLongExactHomologySequenceTarget.{v, u, w} := by
  constructor
  · intro h C _ _ ι c S hS
    refine ⟨(h C ι c S hS).1, ?_, ?_⟩
    · intro i j hij
      exact ((h C ι c S hS).2 i j hij).1
    · intro i j hij
      exact ((h C ι c S hS).2 i j hij).2
  · intro h C _ _ ι c S hS
    refine ⟨(h C ι c S hS).1, ?_⟩
    intro i j hij
    exact ⟨(h C ι c S hS).2.1 i j hij, (h C ι c S hS).2.2 i j hij⟩

-- Structural mutations are compared as explicit kernel expressions by `check_statement.py`.
def mutationRemovedShortExactHypothesis : Prop :=
  ∀ (C : Type u) [Category.{v} C] [Abelian C]
    (ι : Type w) (c : ComplexShape ι)
    (S : ShortComplex (HomologicalComplex C c)),
    ∀ i : ι,
      (ShortComplex.mk
        (HomologicalComplex.homologyMap S.f i)
        (HomologicalComplex.homologyMap S.g i)
        (by
          rw [← HomologicalComplex.homologyMap_comp, S.zero,
            HomologicalComplex.homologyMap_zero])).Exact

def mutationChangedCategoryUniverse : Prop :=
  ∀ (C : Type (u + 1)) [Category.{v} C] [Abelian C]
    (ι : Type w) (c : ComplexShape ι)
    (S : ShortComplex (HomologicalComplex C c)) (hS : S.ShortExact),
    ∀ (i j : ι) (hij : c.Rel i j),
      (ShortComplex.mk
        (HomologicalComplex.homologyMap S.g i)
        (hS.δ i j hij)
        (hS.comp_δ i j hij)).Exact

def mutationChangedBinderScope : Prop :=
  ∀ (C : Type u) [Category.{v} C] [Abelian C]
    (ι : Type w) (c : ComplexShape ι)
    (S : ShortComplex (HomologicalComplex C c)),
    Nonempty S.ShortExact

def mutationSingleAdjacentWindow : Prop :=
  ∀ (C : Type u) [Category.{v} C] [Abelian C]
    (ι : Type w) (c : ComplexShape ι)
    (S : ShortComplex (HomologicalComplex C c)) (hS : S.ShortExact)
    (i j : ι) (hij : c.Rel i j),
    (ShortComplex.mk
      (HomologicalComplex.homologyMap S.g i)
      (hS.δ i j hij)
      (hS.comp_δ i j hij)).Exact

end Stage1Instances.THM_M_0534

set_option pp.explicit true in
#print Stage1Instances.THM_M_0534.LongExactHomologySequenceTarget
