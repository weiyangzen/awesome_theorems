import Mathlib.AlgebraicGeometry.EllipticCurve.Affine.Point
import Mathlib.NumberTheory.Height.NumberField

/-!
# THM-M-0452: exact Neron-Tate pairing statement

This module freezes the pairing, its normalization, and its descent modulo
torsion. It declares only a proposition; it does not construct the pairing.
-/

noncomputable section

open Filter
open scoped Topology WeierstrassCurve.Affine

namespace Stage1Instances.THM_M_0452

universe u

/-- Absolute logarithmic height of the projective x-coordinate, with the point
at infinity represented by mathlib's `[1, 0]` convention. -/
def xHeight {K : Type u} [Field K] [NumberField K]
    {E : WeierstrassCurve K} (P : E⟮K⟯) : ℝ :=
  Height.logHeight P.xRep

/-- The normalized canonical height together with its Neron-Tate polarization.
The limiting formula and bounded comparison distinguish the canonical height
from an arbitrary quadratic form. -/
structure NeronTatePairingPackage (K : Type u) [Field K] [DecidableEq K] [NumberField K]
    (E : WeierstrassCurve K) [E.IsElliptic] where
  canonicalHeight : E⟮K⟯ → ℝ
  limit_formula : ∀ P : E⟮K⟯,
    Tendsto (λ n : ℕ => (4 : ℝ) ^ (-(n : ℤ)) *
      xHeight (((2 : ℕ) ^ n) • P) / 2) atTop (nhds (canonicalHeight P))
  bounded_difference : ∃ C : ℝ, ∀ P : E⟮K⟯,
    |canonicalHeight P - xHeight P / 2| ≤ C
  pairing : E⟮K⟯ → E⟮K⟯ → ℝ
  polarization : ∀ P Q : E⟮K⟯,
    pairing P Q = (canonicalHeight (P + Q) - canonicalHeight P - canonicalHeight Q) / 2
  symmetric : ∀ P Q : E⟮K⟯, pairing P Q = pairing Q P
  add_left : ∀ P Q R : E⟮K⟯, pairing (P + Q) R = pairing P R + pairing Q R
  add_right : ∀ P Q R : E⟮K⟯, pairing P (Q + R) = pairing P Q + pairing P R
  zsmul_left : ∀ (m : ℤ) (P Q : E⟮K⟯), pairing (m • P) Q = (m : ℝ) * pairing P Q
  zsmul_right : ∀ (n : ℤ) (P Q : E⟮K⟯), pairing P (n • Q) = (n : ℝ) * pairing P Q
  self_pairing : ∀ P : E⟮K⟯, pairing P P = canonicalHeight P
  diagonal_nonnegative : ∀ P : E⟮K⟯, 0 ≤ pairing P P
  diagonal_kernel : ∀ P : E⟮K⟯, pairing P P = 0 ↔ IsOfFinAddOrder P
  quotientPairing :
    (E⟮K⟯ ⧸ (AddCommGroup.torsion E⟮K⟯)) →
      (E⟮K⟯ ⧸ (AddCommGroup.torsion E⟮K⟯)) → ℝ
  quotient_lift : ∀ P Q : E⟮K⟯,
    quotientPairing (QuotientAddGroup.mk P) (QuotientAddGroup.mk Q) = pairing P Q
  quotient_positive_definite : ∀ X : E⟮K⟯ ⧸ (AddCommGroup.torsion E⟮K⟯),
    0 ≤ quotientPairing X X ∧ (quotientPairing X X = 0 ↔ X = 0)

/-- Every elliptic curve over every number field admits the normalized
Neron-Tate pairing package, including its positive-definite torsion quotient. -/
def NeronTatePairingTarget : Prop :=
  ∀ {K : Type u} [Field K] [DecidableEq K] [NumberField K],
    ∀ (E : WeierstrassCurve K) [E.IsElliptic],
      Nonempty (NeronTatePairingPackage K E)

-- Structural mutations distinguished by `check_statement.py`.
def mutationRemovedNumberField : Prop :=
  ∀ {K : Type u} [Field K] [DecidableEq K],
    ∀ (E : WeierstrassCurve K) [E.IsElliptic], ∃ b : E⟮K⟯ → E⟮K⟯ → ℝ,
      ∀ P Q, b P Q = b Q P

def mutationChangedPolarizationFactor : Prop :=
  ∀ {K : Type u} [Field K] [DecidableEq K] [NumberField K],
    ∀ (E : WeierstrassCurve K) [E.IsElliptic], ∃ h : E⟮K⟯ → ℝ,
      ∃ b : E⟮K⟯ → E⟮K⟯ → ℝ,
      ∀ P Q, b P Q = h (P + Q) - h P - h Q

def mutationNaturalScalarsOnly : Prop :=
  ∀ {K : Type u} [Field K] [DecidableEq K] [NumberField K],
    ∀ (E : WeierstrassCurve K) [E.IsElliptic], ∃ b : E⟮K⟯ → E⟮K⟯ → ℝ,
      ∀ (m n : ℕ) (P Q), b (m • P) (n • Q) = (m : ℝ) * (n : ℝ) * b P Q

def mutationOmittedTorsionQuotient : Prop :=
  ∀ {K : Type u} [Field K] [DecidableEq K] [NumberField K],
    ∀ (E : WeierstrassCurve K) [E.IsElliptic], ∃ b : E⟮K⟯ → E⟮K⟯ → ℝ,
      ∀ P, 0 ≤ b P P

/-- The identity convention used by the canonical-height normalization. -/
example {K : Type u} [Field K] [NumberField K] {E : WeierstrassCurve K} :
    xHeight (0 : E⟮K⟯) = Height.logHeight (![1, 0] : Fin 2 → K) := by
  simp [xHeight]

end Stage1Instances.THM_M_0452

set_option pp.explicit true in
#print Stage1Instances.THM_M_0452.NeronTatePairingTarget
