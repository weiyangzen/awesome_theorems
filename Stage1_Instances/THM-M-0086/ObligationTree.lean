import Mathlib.CategoryTheory.Abelian.FreydMitchell

/-!
# THM-M-0086 conditional obligation composition

This harness freezes the three independent branches as explicit premises and checks their
composition into the exact unfolded canonical proposition. It deliberately does not invoke the
three terminal mathlib theorems and therefore does not close the root.
-/

noncomputable section

open CategoryTheory CategoryTheory.Limits
open CategoryTheory.Abelian

universe v u

namespace Stage1Instances.THM_M_0086.ObligationTree

def Embedding (C : Type u) [Category.{v} C] [Abelian C] : Prop :=
  ∃ (R : Type (max u v)) (_ : Ring R) (F : C ⥤ ModuleCat.{max u v} R),
    F.Full ∧ F.Faithful ∧ PreservesFiniteLimits F ∧ PreservesFiniteColimits F

def InjectiveCogenerator (C : Type u) [Category.{v} C] [Abelian C] : Prop :=
  ∀ [HasLimits C] [EnoughInjectives C] (G : C),
    IsSeparator G → ∃ I : C, Injective I ∧ IsCoseparator I

def ProjectiveGenerator (C : Type u) [Category.{v} C] [Abelian C] : Prop :=
  ∀ [HasColimits C] [EnoughProjectives C] (G : C),
    IsCoseparator G → ∃ P : C, Projective P ∧ IsSeparator P

def Root : Prop :=
  ∀ (C : Type u) [Category.{v} C] [Abelian C],
    Embedding C ∧ InjectiveCogenerator C ∧ ProjectiveGenerator C

/-- Exact child-to-parent composition. All three universally quantified branch obligations are
consumed; none is proved in this architecture phase. -/
theorem root_compose
    (embedding : ∀ (C : Type u) [Category.{v} C] [Abelian C], Embedding C)
    (injective : ∀ (C : Type u) [Category.{v} C] [Abelian C], InjectiveCogenerator C)
    (projective : ∀ (C : Type u) [Category.{v} C] [Abelian C], ProjectiveGenerator C) :
    Root.{v, u} := by
  intro C _ _
  exact ⟨embedding C, injective C, projective C⟩

#check CategoryTheory.Abelian.freyd_mitchell
#check CategoryTheory.Abelian.has_injective_coseparator
#check CategoryTheory.Abelian.has_projective_separator
#print axioms root_compose

end Stage1Instances.THM_M_0086.ObligationTree
