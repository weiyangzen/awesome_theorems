import Mathlib.AlgebraicGeometry.EllipticCurve.Affine.Point
import Mathlib.GroupTheory.Torsion
import Mathlib.NumberTheory.ModularForms.Cusps

/-!
# THM-M-0442 pinned anchor probe

This module checks the exact mathlib substrate found by the anchor audit. None
of these declarations proves Mazur's rational torsion classification.
-/

noncomputable section

open scoped MatrixGroups WeierstrassCurve.Affine

namespace Stage1Instances.THMM0442.AnchorAudit

abbrev RationalCurve := WeierstrassCurve Rat

abbrev RationalPoint (E : RationalCurve) := E⟮Rat⟯

abbrev RationalTorsion (E : RationalCurve) [E.IsElliptic] :=
  AddCommGroup.torsion E⟮Rat⟯

theorem torsion_membership_uses_finite_additive_order
    (E : RationalCurve) [E.IsElliptic] (P : RationalPoint E) :
    P ∈ AddCommGroup.torsion E⟮Rat⟯ ↔ IsOfFinAddOrder P := by
  exact AddCommGroup.mem_torsion (G := RationalPoint E) P

abbrev GammaZero (N : Nat) : Subgroup SL(2, Int) :=
  CongruenceSubgroup.Gamma0 N

abbrev GammaOne (N : Nat) : Subgroup SL(2, Int) :=
  CongruenceSubgroup.Gamma1 N

abbrev GammaZeroCusps (N : Nat) :=
  CuspOrbits (CongruenceSubgroup.Gamma0 N : Subgroup (GL (Fin 2) Real))

/-- The pinned closure has statement substrate but no audited terminal theorem. -/
def terminalMazurClassificationFound : Bool := false

theorem terminalMazurClassificationFound_eq_false :
    terminalMazurClassificationFound = false := rfl

#check WeierstrassCurve
#check WeierstrassCurve.IsElliptic
#check WeierstrassCurve.Affine.Point
#check AddCommGroup.torsion
#check AddCommGroup.mem_torsion
#check CongruenceSubgroup.Gamma0
#check CongruenceSubgroup.Gamma1
#check CuspOrbits
end Stage1Instances.THMM0442.AnchorAudit
