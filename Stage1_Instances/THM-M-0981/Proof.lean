import Statement
import ObligationTree

/-!
# THM-M-0981 proof-phase bodies

This module integrates the three pinned mathlib terminal declarations and
checks both a direct proof of the exact frozen target and the frozen
child-to-parent composition route.
-/

open Function MeasureTheory Set

namespace Stage1Instances.THM_M_0981.Proof

universe u

/-- Pinned proof body for the empty-event leaf. -/
theorem emptyEventPackage :
    ObligationTree.EmptyEventPackage.{u} := by
  intro Omega _ P
  exact measure_empty

/-- Pinned proof body for the unit-mass leaf, including the frozen conversion
from an explicit probability-measure premise to a local instance. -/
theorem unitMassPackage :
    ObligationTree.UnitMassPackage.{u} := by
  intro Omega _ P hP
  letI : IsProbabilityMeasure P := hP
  exact measure_univ

/-- Pinned proof body for the countable-additivity leaf. -/
theorem countableAdditivityPackage :
    ObligationTree.CountableAdditivityPackage.{u} := by
  intro Omega _ P A hmeas hdisjoint
  exact measure_iUnion hdisjoint hmeas

/-- The frozen composition certificate supplied with all three closed leaf
packages. -/
theorem canonicalRoot_via_frozen_composition
    (Omega : Type u) [MeasurableSpace Omega] :
    ObligationTree.CanonicalRoot Omega :=
  ObligationTree.root_compose emptyEventPackage unitMassPackage
    countableAdditivityPackage Omega

/-- Exact proof of the intake-selected target. The final conversion is only
the transparent unfolding shared by `KolmogorovAxiomsTarget`,
`KolmogorovAxioms`, and the frozen `CanonicalRoot`. -/
theorem kolmogorovAxioms
    (Omega : Type u) [MeasurableSpace Omega] :
    KolmogorovAxiomsTarget Omega := by
  simpa [KolmogorovAxiomsTarget, KolmogorovAxioms,
    ObligationTree.CanonicalRoot] using
      canonicalRoot_via_frozen_composition Omega

#print axioms emptyEventPackage
#print axioms unitMassPackage
#print axioms countableAdditivityPackage
#print axioms canonicalRoot_via_frozen_composition
#print axioms kolmogorovAxioms

end Stage1Instances.THM_M_0981.Proof
