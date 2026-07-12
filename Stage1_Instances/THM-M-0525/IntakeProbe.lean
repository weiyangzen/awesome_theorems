import Mathlib.AlgebraicTopology.FundamentalGroupoid.FundamentalGroup

-- Discovery probe only: the exact target and its credit are deferred to the statement phase.
#check FundamentalGroup
#check FundamentalGroupoid
#check Path.Homotopic.Quotient
#check FundamentalGroupoid.comp_eq
#check FundamentalGroupoid.id_eq_path_refl
#check FundamentalGroup.fundamentalGroupMulEquivOfPath

universe u

section

variable (X : Type u) [TopologicalSpace X] (x : X)

#synth Group (FundamentalGroup X x)

example : FundamentalGroup X x = CategoryTheory.End (FundamentalGroupoid.mk x) := rfl

end
