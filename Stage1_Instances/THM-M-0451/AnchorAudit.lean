import Mathlib.AlgebraicGeometry.EllipticCurve.Affine.Point
import Mathlib.NumberTheory.Height.NumberField

/-!
# THM-M-0451 pinned anchor probes

These checks cover the elliptic-point and global-height infrastructure found in
the pinned mathlib revision.  They do not construct a canonical height or
inhabit `NeronTateCanonicalHeightTarget`.
-/

noncomputable section

open scoped WeierstrassCurve.Affine

namespace Stage1Instances.THM_M_0451.AnchorAudit

universe u

/-- The pinned point API supplies the exact coordinate carrier used by the
frozen statement's naive height. -/
abbrev XCoordinateCarrier {K : Type u} [Field K]
    {E : WeierstrassCurve K} (_P : E⟮K⟯) := Fin 2 -> K

/-- Pinned mathlib proves nonnegativity of the selected tuple log height.  This
is only a property of `xHeight`, not canonical-height nonnegativity. -/
theorem xHeight_nonnegative {K : Type u} [Field K] [NumberField K]
    {E : WeierstrassCurve K} (P : E⟮K⟯) :
    0 <= Height.logHeight P.xRep :=
  Height.logHeight_nonneg P.xRep

/-- The point at infinity uses the exact coordinate convention frozen by the
statement phase. -/
theorem zero_xRep {K : Type u} [Field K] {E : WeierstrassCurve K} :
    (0 : E⟮K⟯).xRep = (![1, 0] : Fin 2 -> K) := by
  simp

#check WeierstrassCurve.Affine.Point.xRep
#check Height.logHeight
#check Height.logHeight_nonneg
#check IsOfFinAddOrder
#check xHeight_nonnegative
#check zero_xRep

end Stage1Instances.THM_M_0451.AnchorAudit
