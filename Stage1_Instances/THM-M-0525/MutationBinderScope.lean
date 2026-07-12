import Mathlib.AlgebraicTopology.FundamentalGroupoid.FundamentalGroup
universe u

-- Expected to fail: `x` cannot be scoped before the type in which it lives.
#check fun (x : X) (X : Type u) [TopologicalSpace X] =>
  Nonempty (Group (Path.Homotopic.Quotient x x))
