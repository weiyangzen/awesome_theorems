import Statement

/-!
# THM-M-0002 independent validation probe

This module reconstructs the exact frozen target through mathlib's pinned
five-lemma declaration. It deliberately does not reuse the proof-phase
wrapper or its explicit two-branch implementation.
-/

noncomputable section

universe u v

namespace Stage1Instances.THM_M_0002.Validation

open CategoryTheory CategoryTheory.ComposableArrows
open Stage1Instances.THM_M_0002

variable {C : Type u} [Category.{v} C] [Abelian C]

/-- Independent exact-type reconstruction of the frozen root. -/
theorem independentFiveLemma : FiveLemmaTarget (C := C) := by
  intro R₁ R₂ phi hR₁ hR₂ h₀ h₁ h₃ h₄
  exact CategoryTheory.Abelian.isIso_of_epi_of_isIso_of_isIso_of_mono
    hR₁ hR₂ phi h₀ h₁ h₃ h₄

#check independentFiveLemma
#print axioms independentFiveLemma

end Stage1Instances.THM_M_0002.Validation
