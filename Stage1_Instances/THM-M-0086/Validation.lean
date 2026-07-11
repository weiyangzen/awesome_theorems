import Statement

/-!
# THM-M-0086 independent validation probe

This module reconstructs the exact frozen package directly from the three pinned mathlib
declarations. It deliberately does not import `Proof.lean` or reuse its wrappers.
-/

noncomputable section

open CategoryTheory CategoryTheory.Limits
open CategoryTheory.Abelian

universe v u

namespace Stage1Instances.THM_M_0086.Validation

open Stage1Instances.THM_M_0086

/-- Same-checkout independent reconstruction of the exact canonical target. -/
theorem independentFreydTheoremPackage : CanonicalStatement.{v, u} := by
  intro C _ _
  refine ⟨CategoryTheory.Abelian.freyd_mitchell C, ?_, ?_⟩
  · intro _ _ G hG
    exact CategoryTheory.Abelian.has_injective_coseparator G hG
  · intro _ _ G hG
    exact CategoryTheory.Abelian.has_projective_separator G hG

#check independentFreydTheoremPackage
#print axioms independentFreydTheoremPackage

end Stage1Instances.THM_M_0086.Validation
