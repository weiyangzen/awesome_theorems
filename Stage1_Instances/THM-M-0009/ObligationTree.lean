import Mathlib.Algebra.Homology.DerivedCategory.Ext.ExactSequences

/-!
# THM-M-0009 conditional obligation composition

This module checks only the composition of the two variance branches into the
frozen root. The branch proofs remain explicit premises of `root_compose`.
-/

universe w v u

namespace Stage1Instances.THM_M_0009.ObligationTree

open CategoryTheory

def CovariantBranch : Prop :=
  ∀ (C : Type u) [Category.{v} C] [Abelian C] [HasExt.{w} C]
    (X : C) (S : ShortComplex C) (hS : S.ShortExact)
    (n₀ n₁ : ℕ) (h : n₀ + 1 = n₁),
    (Abelian.Ext.covariantSequence X hS n₀ n₁ h).Exact

def ContravariantBranch : Prop :=
  ∀ (C : Type u) [Category.{v} C] [Abelian C] [HasExt.{w} C]
    (Y : C) (S : ShortComplex C) (hS : S.ShortExact)
    (n₀ n₁ : ℕ) (h : 1 + n₀ = n₁),
    (Abelian.Ext.contravariantSequence hS Y n₀ n₁ h).Exact

def Root : Prop :=
  ∀ (C : Type u) [Category.{v} C] [Abelian C] [HasExt.{w} C],
    (∀ (X : C) (S : ShortComplex C) (hS : S.ShortExact)
      (n₀ n₁ : ℕ) (h : n₀ + 1 = n₁),
      (Abelian.Ext.covariantSequence X hS n₀ n₁ h).Exact) ∧
    (∀ (Y : C) (S : ShortComplex C) (hS : S.ShortExact)
      (n₀ n₁ : ℕ) (h : 1 + n₀ = n₁),
      (Abelian.Ext.contravariantSequence hS Y n₀ n₁ h).Exact)

/-- The checked child-to-parent edge. No upstream exactness theorem is used. -/
theorem root_compose
    (cov : CovariantBranch.{w, v, u})
    (contra : ContravariantBranch.{w, v, u}) : Root.{w, v, u} := by
  intro C _ _ _
  exact ⟨cov C, contra C⟩

#check Abelian.Ext.covariantSequence_exact
#check Abelian.Ext.contravariantSequence_exact
#print axioms root_compose

end Stage1Instances.THM_M_0009.ObligationTree
