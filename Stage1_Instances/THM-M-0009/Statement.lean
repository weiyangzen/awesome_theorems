import Mathlib.Algebra.Homology.DerivedCategory.Ext.ExactSequences

/-!
# THM-M-0009: long exact sequences of Ext

This module freezes the universally indexed exactness statement in both
arguments of Ext. It contains no proof of the target.
-/

universe w v u

namespace Stage1Instances.THM_M_0009

open CategoryTheory

/-- Every short exact sequence in either argument of Ext induces the
corresponding long exact sequence. Quantification over every pair of
successive natural degrees makes each branch a continuing sequence rather
than one selected six-term window. -/
def LongExactExtSequenceTarget : Prop :=
  ∀ (C : Type u) [Category.{v} C] [Abelian C] [HasExt.{w} C],
    (∀ (X : C) (S : ShortComplex C) (hS : S.ShortExact)
      (n₀ n₁ : ℕ) (h : n₀ + 1 = n₁),
      (Abelian.Ext.covariantSequence X hS n₀ n₁ h).Exact) ∧
    (∀ (Y : C) (S : ShortComplex C) (hS : S.ShortExact)
      (n₀ n₁ : ℕ) (h : 1 + n₀ = n₁),
      (Abelian.Ext.contravariantSequence hS Y n₀ n₁ h).Exact)

/-- An alternate encoding that names the two variance directions separately. -/
def CovariantLongExactExtSequence : Prop :=
  ∀ (C : Type u) [Category.{v} C] [Abelian C] [HasExt.{w} C]
    (X : C) (S : ShortComplex C) (hS : S.ShortExact)
    (n₀ n₁ : ℕ) (h : n₀ + 1 = n₁),
    (Abelian.Ext.covariantSequence X hS n₀ n₁ h).Exact

def ContravariantLongExactExtSequence : Prop :=
  ∀ (C : Type u) [Category.{v} C] [Abelian C] [HasExt.{w} C]
    (Y : C) (S : ShortComplex C) (hS : S.ShortExact)
    (n₀ n₁ : ℕ) (h : 1 + n₀ = n₁),
    (Abelian.Ext.contravariantSequence hS Y n₀ n₁ h).Exact

/-- Checked transport to the encoding with separately named branches. -/
theorem longExactExtSequenceTarget_iff_variance_branches :
    LongExactExtSequenceTarget.{w, v, u} ↔
      CovariantLongExactExtSequence.{w, v, u} ∧
        ContravariantLongExactExtSequence.{w, v, u} := by
  constructor
  · intro h
    constructor
    · intro C _ _ _ X S hS n₀ n₁ hn
      exact (h C).1 X S hS n₀ n₁ hn
    · intro C _ _ _ Y S hS n₀ n₁ hn
      exact (h C).2 Y S hS n₀ n₁ hn
  · rintro ⟨hc, hv⟩ C
    exact ⟨hc C, hv C⟩

-- Structural mutations elaborated independently by `check_statement.py`.
def mutationCovariantOnly : Prop :=
  CovariantLongExactExtSequence.{w, v, u}

def mutationContravariantOnly : Prop :=
  ContravariantLongExactExtSequence.{w, v, u}

def mutationRemovedShortExactHypothesis : Prop :=
  ∀ (C : Type u) [Category.{v} C] [Abelian C] [HasExt.{w} C]
    (S : ShortComplex C),
    Nonempty S.ShortExact

def mutationSingleCovariantWindow : Prop :=
  ∀ (C : Type u) [Category.{v} C] [Abelian C] [HasExt.{w} C]
    (X : C) (S : ShortComplex C) (hS : S.ShortExact),
    (Abelian.Ext.covariantSequence X hS 0 1 rfl).Exact

end Stage1Instances.THM_M_0009

set_option pp.explicit true in
#print Stage1Instances.THM_M_0009.LongExactExtSequenceTarget
