import Statement

/-!
# THM-M-0353 conditional obligation composition

This module checks only the final composition boundary of the frozen proof
architecture. Both analytic packages are explicit assumptions, so this is not
a proof of Hermite completeness.
-/

namespace Stage1Instances.THM_M_0353

open scoped ENNReal
open MeasureTheory

/-- Every literal normalized Hermite function represents an `L^2` vector. -/
def HermiteMemLpPackage : Prop :=
  forall n : Nat, MemLp (hermiteFunction n) (2 : ENNReal) leb

/-- The represented Hermite vectors are packaged as the requested Hilbert basis. -/
def HermiteBasisPackage : Prop :=
  exists b : HilbertBasis Nat Complex (Lp Complex (2 : ENNReal) leb),
    forall n : Nat, (b n : Real -> Complex) =ᵐ[leb] hermiteFunction n

/-- Kernel-checked conjunction assembly for the exact canonical target. -/
theorem root_of_hermite_packages
    (memLp : HermiteMemLpPackage)
    (basis : HermiteBasisPackage) :
    HermiteCompletenessTarget :=
  And.intro memLp basis

#print axioms root_of_hermite_packages

end Stage1Instances.THM_M_0353
