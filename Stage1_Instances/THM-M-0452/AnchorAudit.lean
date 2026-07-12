import Mathlib.AlgebraicGeometry.EllipticCurve.Affine.Point
import Mathlib.NumberTheory.Height.NumberField

/-!
# THM-M-0452 pinned anchor probes

These checks cover the point group, naive logarithmic height, torsion subgroup,
and quotient substrate at the pinned mathlib revision. They do not construct a
canonical height or a Neron-Tate pairing.
-/

noncomputable section

open scoped WeierstrassCurve.Affine

namespace Stage1Instances.THM_M_0452.AnchorAudit

universe u

/-- The selected logarithmic x-height is nonnegative. This is not a theorem
about the missing canonical height. -/
theorem xHeight_nonnegative {K : Type u} [Field K] [NumberField K]
    {E : WeierstrassCurve K} (P : E⟮K⟯) :
    0 <= Height.logHeight P.xRep :=
  Height.logHeight_nonneg P.xRep

/-- Mathlib's torsion subgroup has exactly the membership predicate used by
the frozen diagonal-kernel statement. -/
theorem mem_torsion_iff {G : Type u} [AddCommGroup G] (P : G) :
    P ∈ AddCommGroup.torsion G ↔ IsOfFinAddOrder P :=
  Iff.rfl

/-- The quotient constructor needed by the frozen descended pairing exists
for the exact torsion subgroup. -/
def torsionQuotientClass {G : Type u} [AddCommGroup G] (P : G) :
    G ⧸ AddCommGroup.torsion G :=
  QuotientAddGroup.mk P

/-- The identity-point coordinate convention agrees with the statement. -/
theorem zero_xRep {K : Type u} [Field K] {E : WeierstrassCurve K} :
    (0 : E⟮K⟯).xRep = (![1, 0] : Fin 2 → K) := by
  simp

#check WeierstrassCurve.Affine.Point.xRep
#check Height.logHeight
#check Height.logHeight_nonneg
#check AddCommGroup.torsion
#check QuotientAddGroup.mk
#check IsOfFinAddOrder
#check xHeight_nonnegative
#check mem_torsion_iff
#check torsionQuotientClass
#check zero_xRep

end Stage1Instances.THM_M_0452.AnchorAudit
