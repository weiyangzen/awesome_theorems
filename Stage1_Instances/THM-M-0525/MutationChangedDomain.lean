import Mathlib.AlgebraicTopology.FundamentalGroupoid.FundamentalGroup
universe u

-- Expected to fail: the basepoint must inhabit the same space as the loop carrier.
#check fun (X Y : Type u) [TopologicalSpace X] (x : Y) =>
  Nonempty (Group (Path.Homotopic.Quotient (X := X) x x))
