import Mathlib.CategoryTheory.Abelian.FreydMitchell

/-!
# THM-M-0086 pinned anchor probes

The named theorem below checks that the three terminal declarations found in
the pinned mathlib snapshot compose to the fully unfolded canonical target.
It is audit evidence only, not the proof-phase canonical wrapper.
-/

noncomputable section

open CategoryTheory CategoryTheory.Limits
open CategoryTheory.Abelian

universe v u

namespace Stage1Instances.THM_M_0086.AnchorAudit

#check CategoryTheory.Abelian.freyd_mitchell
#check CategoryTheory.Abelian.has_injective_coseparator
#check CategoryTheory.Abelian.has_projective_separator

theorem pinned_mathlib_closes_unfolded_target :
    ∀ (C : Type u) [Category.{v} C] [Abelian C],
      (∃ (R : Type (max u v)) (_ : Ring R) (F : C ⥤ ModuleCat.{max u v} R),
          F.Full ∧ F.Faithful ∧ PreservesFiniteLimits F ∧ PreservesFiniteColimits F) ∧
      (∀ [HasLimits C] [EnoughInjectives C] (G : C),
          IsSeparator G → ∃ I : C, Injective I ∧ IsCoseparator I) ∧
      (∀ [HasColimits C] [EnoughProjectives C] (G : C),
          IsCoseparator G → ∃ P : C, Projective P ∧ IsSeparator P) := by
  intro C _ _
  exact ⟨CategoryTheory.Abelian.freyd_mitchell C,
    fun G hG => CategoryTheory.Abelian.has_injective_coseparator G hG,
    fun G hG => CategoryTheory.Abelian.has_projective_separator G hG⟩

#print axioms CategoryTheory.Abelian.freyd_mitchell
#print axioms CategoryTheory.Abelian.has_injective_coseparator
#print axioms CategoryTheory.Abelian.has_projective_separator
#print axioms pinned_mathlib_closes_unfolded_target

end Stage1Instances.THM_M_0086.AnchorAudit
