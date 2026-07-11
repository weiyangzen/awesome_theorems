import Statement

/-!
# THM-M-0002: proof of the categorical five lemma target

The proof imports the exact frozen target through an isolated, temporary
`Statement.olean` built by `check_proof.sh`. It exposes both four-lemma
branches rather than hiding them behind the upstream five-lemma wrapper.
-/

noncomputable section

universe u v

namespace Stage1Instances.THM_M_0002.Proof

open CategoryTheory CategoryTheory.ComposableArrows
open Stage1Instances.THM_M_0002

variable {C : Type u} [Category.{v} C] [Abelian C]

/-- In a morphism between exact five-object rows, epi/iso/iso/mono vertical
hypotheses imply that the middle vertical morphism is an isomorphism. -/
theorem fiveLemma : FiveLemmaTarget (C := C) := by
  intro R₁ R₂ phi hR₁ hR₂ h₀ h₁ h₃ h₄
  dsimp at h₀ h₁ h₃ h₄
  have middleMono : Mono (app' phi 2) := by
    apply CategoryTheory.Abelian.mono_of_epi_of_mono_of_mono
      (δlastFunctor.map phi) (R₁.exact_iff_δlast.1 hR₁).1
      (R₂.exact_iff_δlast.1 hR₂).1 <;> dsimp <;> infer_instance
  have middleEpi : Epi (app' phi 2) := by
    apply CategoryTheory.Abelian.epi_of_epi_of_epi_of_mono
      (δ₀Functor.map phi) (R₁.exact_iff_δ₀.1 hR₁).2
      (R₂.exact_iff_δ₀.1 hR₂).2 <;> dsimp <;> infer_instance
  apply CategoryTheory.isIso_of_mono_of_epi

#print axioms fiveLemma

end Stage1Instances.THM_M_0002.Proof
