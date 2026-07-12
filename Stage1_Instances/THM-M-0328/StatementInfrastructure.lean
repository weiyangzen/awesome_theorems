import Mathlib.Analysis.Normed.Module.PiTensorProduct.InjectiveSeminorm

/-!
# THM-M-0328 statement-infrastructure probe

This file checks the strongest directly relevant tensor-product comparison in
the pinned mathlib snapshot. It is not the canonical Grothendieck-duality
target: the snapshot has neither the required nuclear locally convex-space
object model nor completed projective and injective locally convex tensor
products.
-/

noncomputable section

open scoped TensorProduct

namespace Stage1Instances.THM_M_0328

universe uι u𝕜 uE

variable {ι : Type uι} [Fintype ι]
variable {𝕜 : Type u𝕜} [NontriviallyNormedField 𝕜]
variable {E : ι → Type uE}
variable [∀ i, SeminormedAddCommGroup (E i)] [∀ i, NormedSpace 𝕜 (E i)]

/-- The pinned finite algebraic substrate compares the two available seminorms. -/
theorem finite_injective_le_projective :
    PiTensorProduct.injectiveSeminorm (𝕜 := 𝕜) (E := E) ≤
      PiTensorProduct.projectiveSeminorm (𝕜 := 𝕜) (E := E) :=
  PiTensorProduct.injectiveSeminorm_le_projectiveSeminorm

#check PiTensorProduct.injectiveSeminorm
#check PiTensorProduct.projectiveSeminorm
#check finite_injective_le_projective

end Stage1Instances.THM_M_0328
