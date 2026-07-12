import Mathlib.Analysis.Normed.Module.PiTensorProduct.InjectiveSeminorm
import Mathlib.Analysis.Normed.Module.PiTensorProduct.ProjectiveSeminorm

/-!
# THM-M-0325: pinned anchor audit

These checks validate the closest tensor-seminorm substrate in the pinned
mathlib revision. None of these declarations is Grothendieck's inequality.
-/

noncomputable section

#check PiTensorProduct.projectiveSeminorm
#check PiTensorProduct.projectiveSeminorm_tprod_le
#check PiTensorProduct.injectiveSeminorm
#check PiTensorProduct.norm_eval_le_injectiveSeminorm
#check PiTensorProduct.injectiveSeminorm_le_projectiveSeminorm

namespace Stage1Instances.THM_M_0325

universe u v w

/-- Exact local type check for the pinned projective-seminorm anchor. -/
abbrev auditedProjectiveSeminorm
    {ι : Type u} [Fintype ι]
    {𝕜 : Type v} [NormedField 𝕜]
    {E : ι -> Type w} [forall i, SeminormedAddCommGroup (E i)]
    [forall i, NormedSpace 𝕜 (E i)] :
    Seminorm 𝕜 (PiTensorProduct 𝕜 E) :=
  PiTensorProduct.projectiveSeminorm

/-- The generic comparison available upstream has the opposite role from the
missing Grothendieck estimate: injective seminorm is bounded by projective. -/
theorem auditedInjectiveLeProjective
    {ι : Type u} [Fintype ι]
    {𝕜 : Type v} [NontriviallyNormedField 𝕜]
    {E : ι -> Type w} [forall i, SeminormedAddCommGroup (E i)]
    [forall i, NormedSpace 𝕜 (E i)] :
    PiTensorProduct.injectiveSeminorm (𝕜 := 𝕜) (E := E) <=
      PiTensorProduct.projectiveSeminorm :=
  PiTensorProduct.injectiveSeminorm_le_projectiveSeminorm

#print axioms auditedInjectiveLeProjective

end Stage1Instances.THM_M_0325
