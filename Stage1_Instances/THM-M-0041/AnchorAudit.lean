import Mathlib.LinearAlgebra.Charpoly.Basic

/-!
# THM-M-0041 pinned anchor audit

This standalone probe repeats the frozen expanded-determinant target and checks its exact
definitional transport to mathlib's matrix Cayley-Hamilton theorem. The linear-map declaration is
also inspected as a related encoding; it is not credited as a second terminal proof body.
-/

namespace Stage1Instances.THM_M_0041_AnchorAudit

universe u v

noncomputable section

/-- Audit-local copy of the frozen characteristic-polynomial expression. -/
def characteristicPolynomial {R : Type u} [CommRing R]
    {n : Type v} [DecidableEq n] [Fintype n] (A : Matrix n n R) : Polynomial R :=
  Matrix.det (Matrix.scalar n Polynomial.X - A.map Polynomial.C)

/-- Audit-local copy of the exact statement-gate target. -/
def CanonicalTarget : Prop :=
  forall {R : Type u} [CommRing R] {n : Type v} [DecidableEq n] [Fintype n]
      (A : Matrix n n R),
    Polynomial.aeval A (characteristicPolynomial A) = 0

/-- The expanded local definition and mathlib's `Matrix.charpoly` are definitionally equal. -/
theorem characteristicPolynomial_eq_charpoly {R : Type u} [CommRing R]
    {n : Type v} [DecidableEq n] [Fintype n] (A : Matrix n n R) :
    characteristicPolynomial A = Matrix.charpoly A :=
  rfl

/-- Exact checked wrapper around the pinned mathlib terminal theorem. -/
theorem exactMathlibAnchor : CanonicalTarget.{u, v} := by
  intro R _ n _ _ A
  exact Matrix.aeval_self_charpoly A

#check Matrix.charmatrix
#check Matrix.charpoly
#check Matrix.aeval_self_charpoly
#check LinearMap.charpoly
#check LinearMap.aeval_self_charpoly

end

end Stage1Instances.THM_M_0041_AnchorAudit

set_option pp.universes true in
set_option pp.explicit true in
#print Stage1Instances.THM_M_0041_AnchorAudit.exactMathlibAnchor

#print axioms Stage1Instances.THM_M_0041_AnchorAudit.exactMathlibAnchor
#print axioms Matrix.aeval_self_charpoly
#print axioms LinearMap.aeval_self_charpoly
