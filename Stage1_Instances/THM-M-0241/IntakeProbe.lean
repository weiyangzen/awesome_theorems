import Mathlib.AlgebraicTopology.FundamentalGroupoid.FundamentalGroup
import Mathlib.Analysis.Complex.Basic
import Mathlib.Topology.Compactification.OnePoint.ProjectiveLine

/-!
Discovery-only substrate checks for a later source-selected Riemann-Hilbert statement.

This file defines only a type for possible monodromy input. It deliberately does not define a
regular-singular differential system, a realization predicate, or a target theorem.
-/

namespace Stage1Instances.THM_M_0241

/-- The one-point compactified complex plane with a chosen singular set removed. -/
abbrev PuncturedSphere (singularities : Set (OnePoint ℂ)) :=
  {z : OnePoint ℂ // z ∉ singularities}

/-- A checked type for finite-dimensional complex monodromy representations. -/
abbrev MonodromyRepresentation
    (singularities : Set (OnePoint ℂ))
    (basepoint : PuncturedSphere singularities) (rank : Nat) :=
  FundamentalGroup (PuncturedSphere singularities) basepoint →*
    Matrix.GeneralLinearGroup (Fin rank) ℂ

#check OnePoint ℂ
#check PuncturedSphere
#check FundamentalGroup
#check Matrix.GeneralLinearGroup
#check MonodromyRepresentation

end Stage1Instances.THM_M_0241
