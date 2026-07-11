import Mathlib.CategoryTheory.Abelian.GrothendieckCategory.ModuleEmbedding.GabrielPopescu

/-!
# THM-M-0087 conditional obligation composition

This file kernel-checks only the composition of the four conclusion packages in
the frozen statement.  Each mathematical package remains an explicit premise;
the imported Gabriel-Popescu bodies are not credited by this architecture node.
-/

noncomputable section

open CategoryTheory CategoryTheory.Limits

universe v u

namespace Stage1Instances.THM_M_0087.ObligationTree

variable (C : Type u) [Category.{v} C] [Abelian C]
  [IsGrothendieckAbelian.{v} C]

def Root : Prop :=
  forall G : C, IsSeparator G ->
    (preadditiveCoyonedaObj G).Full /\
    (preadditiveCoyonedaObj G).Faithful /\
    Nonempty
      (IsGrothendieckAbelian.tensorObj G ⊣ preadditiveCoyonedaObj G) /\
    PreservesFiniteLimits (IsGrothendieckAbelian.tensorObj G)

def FullPackage : Prop :=
  forall G : C, IsSeparator G -> (preadditiveCoyonedaObj G).Full

def FaithfulPackage : Prop :=
  forall G : C, IsSeparator G -> (preadditiveCoyonedaObj G).Faithful

def AdjunctionPackage : Prop :=
  forall G : C, IsSeparator G ->
    Nonempty (IsGrothendieckAbelian.tensorObj G ⊣ preadditiveCoyonedaObj G)

def FiniteLimitsPackage : Prop :=
  forall G : C, IsSeparator G ->
    PreservesFiniteLimits (IsGrothendieckAbelian.tensorObj G)

/-- Exact child-to-parent composition.  This proves no package premise. -/
theorem root_of_packages
    (full : FullPackage C)
    (faithful : FaithfulPackage C)
    (adjunction : AdjunctionPackage C)
    (finiteLimits : FiniteLimitsPackage C) : Root C := by
  intro G hG
  exact ⟨full G hG, faithful G hG, adjunction G hG, finiteLimits G hG⟩

theorem root_exact_type :
    Root C =
      (forall G : C, IsSeparator G ->
        (preadditiveCoyonedaObj G).Full /\
        (preadditiveCoyonedaObj G).Faithful /\
        Nonempty
          (IsGrothendieckAbelian.tensorObj G ⊣ preadditiveCoyonedaObj G) /\
        PreservesFiniteLimits (IsGrothendieckAbelian.tensorObj G)) :=
  rfl

#print root_of_packages
#print axioms root_of_packages

end Stage1Instances.THM_M_0087.ObligationTree
