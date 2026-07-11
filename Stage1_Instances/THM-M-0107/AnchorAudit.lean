import Mathlib.AlgebraicGeometry.ZariskisMainTheorem

/-!
# THM-M-0107 immutable mathlib anchor audit

This module checks the three pinned mathlib surfaces needed by the frozen
factorization target. It inventories candidates; acceptance as a proof of the
root belongs to the later proof and validation phases.
-/

open CategoryTheory

namespace Stage1Instances.THM_M_0107.AnchorAudit

open AlgebraicGeometry

universe u

variable {X Y : Scheme.{u}} (f : X ⟶ Y)

#check Scheme.Hom.exists_isIso_morphismRestrict_toNormalization
#check Scheme.Hom.toNormalization_fromNormalization
#check AlgebraicGeometry.IsFinite.of_isProper_of_locallyQuasiFinite

/-- The pinned ZMT instance has exactly the open-immersion component required
by the canonical relative-normalization candidate. -/
example [LocallyQuasiFinite f] [LocallyOfFiniteType f] [IsSeparated f] [QuasiCompact f] :
    IsOpenImmersion f.toNormalization := by
  infer_instance

/-- The normalization API supplies the factorization equation in the same
orientation as the frozen target. -/
example [IsSeparated f] [QuasiCompact f] : f.toNormalization ≫ f.fromNormalization = f :=
  f.toNormalization_fromNormalization

end Stage1Instances.THM_M_0107.AnchorAudit
