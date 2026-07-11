import Mathlib.CategoryTheory.Abelian.GrothendieckCategory.ModuleEmbedding.GabrielPopescu

/-!
# THM-M-0087: pinned anchor audit

The declarations below check the exact mathlib anchors used by the frozen
statement. The final wrapper is an exact candidate check, not a theorem-release
claim.
-/

noncomputable section

open CategoryTheory CategoryTheory.Limits

universe v u

namespace Stage1Instances.THM_M_0087

#check IsGrothendieckAbelian.tensorObj
#check IsGrothendieckAbelian.tensorObjPreadditiveCoyonedaObjAdjunction
#check IsGrothendieckAbelian.GabrielPopescu.full
#check IsGrothendieckAbelian.GabrielPopescu.preservesInjectiveObjects
#check IsGrothendieckAbelian.GabrielPopescu.preservesFiniteLimits
#check isSeparator_iff_faithful_preadditiveCoyonedaObj

variable (C : Type u) [Category.{v} C] [Abelian C]
  [IsGrothendieckAbelian.{v} C]

/-- A local copy of the frozen target, needed because dossier files are checked directly. -/
def AuditedStatement : Prop :=
  ∀ G : C, IsSeparator G →
    (preadditiveCoyonedaObj G).Full ∧
    (preadditiveCoyonedaObj G).Faithful ∧
    Nonempty
      (IsGrothendieckAbelian.tensorObj G ⊣ preadditiveCoyonedaObj G) ∧
    PreservesFiniteLimits (IsGrothendieckAbelian.tensorObj G)

/-- Exact-type integration probe assembled only from the pinned mathlib anchors. -/
theorem exactMathlibCandidate : AuditedStatement C := by
  intro G hG
  exact
    ⟨IsGrothendieckAbelian.GabrielPopescu.full G hG,
      (isSeparator_iff_faithful_preadditiveCoyonedaObj G).1 hG,
      ⟨IsGrothendieckAbelian.tensorObjPreadditiveCoyonedaObjAdjunction G⟩,
      IsGrothendieckAbelian.GabrielPopescu.preservesFiniteLimits G hG⟩

#check exactMathlibCandidate
#print axioms exactMathlibCandidate

end Stage1Instances.THM_M_0087
