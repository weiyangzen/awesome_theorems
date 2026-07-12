import Statement

/-!
# THM-M-1527 conditional obligation composition

This module checks the propositional assembly boundary selected by the frozen
architecture. The two coordinate-decomposition equivalences remain explicit
premises; this file does not assert the canonical root.
-/

namespace Stage1Instances.THM_M_1527

universe u

/-- Checked recombination of the two component packages into the classical /
covariant equivalence. The geometric coordinate calculation is not proved here. -/
theorem assemble_from_component_equivalences
    {Spacetime : Type u} [NormedAddCommGroup Spacetime]
    [NormedSpace Real Spacetime]
    (ops : ClassicalOperators) (c : SIConstants) (classical : ClassicalFields)
    (covariant : CovariantFields Spacetime)
    (homogeneous_iff : Homogeneous covariant <->
      GaussMagnetic ops classical /\ Faraday ops classical)
    (inhomogeneous_iff : Inhomogeneous covariant <->
      GaussElectric ops c classical /\ AmpereMaxwell ops c classical) :
    ClassicalMaxwellSystem ops c classical <-> CovariantMaxwellSystem covariant := by
  constructor
  · rintro ⟨gaussElectric, gaussMagnetic, faraday, ampereMaxwell⟩
    exact ⟨homogeneous_iff.mpr ⟨gaussMagnetic, faraday⟩,
      inhomogeneous_iff.mpr ⟨gaussElectric, ampereMaxwell⟩⟩
  · rintro ⟨homogeneous, inhomogeneous⟩
    obtain ⟨gaussMagnetic, faraday⟩ := homogeneous_iff.mp homogeneous
    obtain ⟨gaussElectric, ampereMaxwell⟩ := inhomogeneous_iff.mp inhomogeneous
    exact ⟨gaussElectric, gaussMagnetic, faraday, ampereMaxwell⟩

#print axioms assemble_from_component_equivalences

end Stage1Instances.THM_M_1527
