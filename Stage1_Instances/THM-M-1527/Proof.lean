import ObligationTree

/-!
# THM-M-1527 proof bodies

This module discharges the exact conditional target frozen in `Statement.lean`.
The coordinate-decomposition equivalences are fields of the target's explicit
`CoordinateDecomposition` premise; the proof projects them and applies the
checked propositional assembly theorem.
-/

noncomputable section

namespace Stage1Instances.THM_M_1527

universe u

/-- The homogeneous coordinate bridge supplied by the target's explicit
coordinate-decomposition premise. -/
theorem homogeneous_iff_of_coordinateDecomposition
    {Spacetime : Type u} [NormedAddCommGroup Spacetime]
    [NormedSpace Real Spacetime]
    (ops : ClassicalOperators) (c : SIConstants) (classical : ClassicalFields)
    (covariant : CovariantFields Spacetime)
    (decomposition : CoordinateDecomposition ops c classical covariant) :
    Homogeneous covariant <->
      GaussMagnetic ops classical /\ Faraday ops classical :=
  decomposition.homogeneous_iff

/-- The inhomogeneous coordinate bridge supplied by the target's explicit
coordinate-decomposition premise. -/
theorem inhomogeneous_iff_of_coordinateDecomposition
    {Spacetime : Type u} [NormedAddCommGroup Spacetime]
    [NormedSpace Real Spacetime]
    (ops : ClassicalOperators) (c : SIConstants) (classical : ClassicalFields)
    (covariant : CovariantFields Spacetime)
    (decomposition : CoordinateDecomposition ops c classical covariant) :
    Inhomogeneous covariant <->
      GaussElectric ops c classical /\ AmpereMaxwell ops c classical :=
  decomposition.inhomogeneous_iff

/-- Exact proof of the frozen conditional Maxwell coordinate equivalence. -/
theorem maxwell_coordinate_equivalence : MaxwellCoordinateEquivalence.{u} := by
  intro Spacetime _ _ ops c classical covariant _ _ _ _ _ decomposition
  exact assemble_from_component_equivalences ops c classical covariant
    (homogeneous_iff_of_coordinateDecomposition ops c classical covariant decomposition)
    (inhomogeneous_iff_of_coordinateDecomposition ops c classical covariant decomposition)

#print axioms homogeneous_iff_of_coordinateDecomposition
#print axioms inhomogeneous_iff_of_coordinateDecomposition
#print axioms maxwell_coordinate_equivalence

end Stage1Instances.THM_M_1527
