import Mathlib.Algebra.Homology.DerivedCategory.Ext.ExactSequences

/-!
# THM-M-0009 pinned mathlib anchor audit

This file checks that the two exactness declarations in the pinned mathlib
revision have precisely the two branch types frozen by `Statement.lean`.
-/

universe w v u

namespace Stage1Instances.THM_M_0009.AnchorAudit

open CategoryTheory

/-- Exact-type adapter for the pinned covariant mathlib candidate. -/
theorem covariantCandidate :
    ∀ (C : Type u) [Category.{v} C] [Abelian C] [HasExt.{w} C]
      (X : C) (S : ShortComplex C) (hS : S.ShortExact)
      (n₀ n₁ : ℕ) (h : n₀ + 1 = n₁),
      (Abelian.Ext.covariantSequence X hS n₀ n₁ h).Exact := by
  intro C _ _ _ X S hS n₀ n₁ h
  exact Abelian.Ext.covariantSequence_exact X hS n₀ n₁ h

/-- Exact-type adapter for the pinned contravariant mathlib candidate. -/
theorem contravariantCandidate :
    ∀ (C : Type u) [Category.{v} C] [Abelian C] [HasExt.{w} C]
      (Y : C) (S : ShortComplex C) (hS : S.ShortExact)
      (n₀ n₁ : ℕ) (h : 1 + n₀ = n₁),
      (Abelian.Ext.contravariantSequence hS Y n₀ n₁ h).Exact := by
  intro C _ _ _ Y S hS n₀ n₁ h
  exact Abelian.Ext.contravariantSequence_exact hS Y n₀ n₁ h

#print axioms covariantCandidate
#print axioms contravariantCandidate

end Stage1Instances.THM_M_0009.AnchorAudit
