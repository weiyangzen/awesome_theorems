import Mathlib.Analysis.Normed.Module.Bases

/-!
# THM-M-0324 anchor audit

This file checks the useful declarations found in pinned mathlib. None has the
existential type of `EnfloNoSchauderBasisTarget`: they provide the Schauder
basis object model and consequences of an already supplied basis.
-/

#check GeneralSchauderBasis
#check SchauderBasis
#check GeneralSchauderBasis.linearIndependent
#check GeneralSchauderBasis.proj
#check GeneralSchauderBasis.range_proj_eq_span
#check GeneralSchauderBasis.finrank_range_proj
#check SchauderBasis.proj
#check SchauderBasis.tendsto_proj
#check SchauderBasis.exists_norm_proj_le
