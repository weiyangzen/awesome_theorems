import Mathlib.AlgebraicTopology.FundamentalGroupoid.FundamentalGroup
import Mathlib.Analysis.Complex.Basic
import Mathlib.Topology.Compactification.OnePoint.ProjectiveLine

/-!
Elaboration probe for the THM-M-1559 exact-statement blocker.

This file checks only the pinned topology and linear-group substrates for the
historical monodromy-realization problem. It deliberately does not define a
Riemann-Hilbert target: neither the source record nor the pinned libraries fix
the required regular-singular connection and realization relation.
-/

namespace Stage1Instances.THM_M_1559

/-- A checked carrier for the Riemann sphere with a chosen singular set removed. -/
abbrev PuncturedSphere (singularities : Set (OnePoint ℂ)) :=
  {z : OnePoint ℂ // z ∉ singularities}

#check OnePoint ℂ
#check FundamentalGroup
#check Matrix.GeneralLinearGroup

/-- The type of finite-dimensional complex monodromy representations available
from the independent pinned fundamental-group and general-linear-group APIs. -/
abbrev MonodromyRepresentation
    (singularities : Set (OnePoint ℂ))
    (basepoint : PuncturedSphere singularities) (rank : Nat) :=
  FundamentalGroup (PuncturedSphere singularities) basepoint →*
    Matrix.GeneralLinearGroup (Fin rank) ℂ

#check MonodromyRepresentation

end Stage1Instances.THM_M_1559
