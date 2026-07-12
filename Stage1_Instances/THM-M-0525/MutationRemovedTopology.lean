import Mathlib.AlgebraicTopology.FundamentalGroupoid.FundamentalGroup
universe u

-- Expected to fail: removing the topology makes based paths and their homotopies unavailable.
#check fun (X : Type u) (x : X) => Nonempty (Group (Path.Homotopic.Quotient x x))
