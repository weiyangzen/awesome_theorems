import Mathlib.Analysis.Normed.Module.Bases

-- These checks establish the representation boundary, not Enflo's existential theorem.
#check SchauderBasis
#check SchauderBasis.proj
#check SchauderBasis.tendsto_proj
#check SchauderBasis.finrank_range_proj
#check SchauderBasis.exists_norm_proj_le

section

variable (K X : Type*) [NontriviallyNormedField K]
variable [NormedAddCommGroup X] [NormedSpace K X] [CompleteSpace X]

#check (show Prop from Nonempty (SchauderBasis K X))
#check (show Prop from ¬ Nonempty (SchauderBasis K X))

end
