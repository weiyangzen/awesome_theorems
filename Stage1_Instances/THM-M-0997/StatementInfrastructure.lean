import Mathlib.Geometry.Manifold.Instances.Sphere
import Mathlib.MeasureTheory.Measure.Hausdorff

/-!
# THM-M-0997 statement-infrastructure probe

This file checks only the pinned sphere and Hausdorff-measure object model. It
does not define a canonical target for Levy's spherical isoperimetric theorem:
the repository source does not identify an exact source formulation, and the
pinned API does not supply the required intrinsic geodesic metric together
with normalized Riemannian surface measure.
-/

noncomputable section

open MeasureTheory
open scoped ENNReal

namespace Stage1Instances.THM_M_0997

/-- The available unit-sphere subtype, used only to probe the pinned API. -/
abbrev AvailableUnitSphere (n : Nat) : Type :=
  Metric.sphere (0 : EuclideanSpace Real (Fin (n + 1))) 1

/-- The Borel measurable structure needed by the Hausdorff-measure probe. -/
instance availableUnitSphereMeasurableSpace (n : Nat) :
    MeasurableSpace (AvailableUnitSphere n) :=
  borel (AvailableUnitSphere n)

instance availableUnitSphereBorelSpace (n : Nat) :
    BorelSpace (AvailableUnitSphere n) :=
  ⟨rfl⟩

/-- The available intrinsic Hausdorff measure on the subtype metric. This is
not asserted to be the normalized Riemannian surface measure of the source
theorem. -/
def availableHausdorffMeasure (n : Nat) : Measure (AvailableUnitSphere n) :=
  (μH[n] : Measure (AvailableUnitSphere n))

#check AvailableUnitSphere
#check availableHausdorffMeasure
#check Metric.closedBall

end Stage1Instances.THM_M_0997
