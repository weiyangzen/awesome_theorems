import Statement

/-!
# THM-M-0452 conditional obligation composition

The three interfaces below expose the semantic construction boundaries of the
frozen proof architecture.  The final theorem composes them into the exact
statement; it does not provide any of the three open packages.
-/

noncomputable section

open Filter
open scoped Topology WeierstrassCurve.Affine

namespace Stage1Instances.THM_M_0452

universe u

structure CanonicalHeightCore (K : Type u) [Field K] [DecidableEq K] [NumberField K]
    (E : WeierstrassCurve K) [E.IsElliptic] where
  canonicalHeight : E⟮K⟯ → ℝ
  limit_formula : ∀ P : E⟮K⟯,
    Tendsto (fun n : ℕ => (4 : ℝ) ^ (-(n : ℤ)) *
      xHeight (((2 : ℕ) ^ n) • P) / 2) atTop (nhds (canonicalHeight P))
  bounded_difference : ∃ C : ℝ, ∀ P : E⟮K⟯,
    |canonicalHeight P - xHeight P / 2| ≤ C

structure PolarizationCore (K : Type u) [Field K] [DecidableEq K] [NumberField K]
    (E : WeierstrassCurve K) [E.IsElliptic] (height : E⟮K⟯ → ℝ) where
  pairing : E⟮K⟯ → E⟮K⟯ → ℝ
  polarization : ∀ P Q, pairing P Q = (height (P + Q) - height P - height Q) / 2
  symmetric : ∀ P Q, pairing P Q = pairing Q P
  add_left : ∀ P Q R, pairing (P + Q) R = pairing P R + pairing Q R
  add_right : ∀ P Q R, pairing P (Q + R) = pairing P Q + pairing P R
  zsmul_left : ∀ (m : ℤ) P Q, pairing (m • P) Q = (m : ℝ) * pairing P Q
  zsmul_right : ∀ (n : ℤ) P Q, pairing P (n • Q) = (n : ℝ) * pairing P Q
  self_pairing : ∀ P, pairing P P = height P
  diagonal_nonnegative : ∀ P, 0 ≤ pairing P P
  diagonal_kernel : ∀ P, pairing P P = 0 ↔ IsOfFinAddOrder P

structure QuotientPairingCore (K : Type u) [Field K] [DecidableEq K] [NumberField K]
    (E : WeierstrassCurve K) [E.IsElliptic] (pairing : E⟮K⟯ → E⟮K⟯ → ℝ) where
  quotientPairing :
    (E⟮K⟯ ⧸ AddCommGroup.torsion E⟮K⟯) →
      (E⟮K⟯ ⧸ AddCommGroup.torsion E⟮K⟯) → ℝ
  quotient_lift : ∀ P Q,
    quotientPairing (QuotientAddGroup.mk P) (QuotientAddGroup.mk Q) = pairing P Q
  quotient_positive_definite : ∀ X : E⟮K⟯ ⧸ AddCommGroup.torsion E⟮K⟯,
    0 ≤ quotientPairing X X ∧ (quotientPairing X X = 0 ↔ X = 0)

def CanonicalHeightCoreTarget : Prop :=
  ∀ {K : Type u} [Field K] [DecidableEq K] [NumberField K],
    ∀ (E : WeierstrassCurve K) [E.IsElliptic], Nonempty (CanonicalHeightCore K E)

def PolarizationCoreTarget : Prop :=
  ∀ {K : Type u} [Field K] [DecidableEq K] [NumberField K],
    ∀ (E : WeierstrassCurve K) [E.IsElliptic] (h : CanonicalHeightCore K E),
      Nonempty (PolarizationCore K E h.canonicalHeight)

def QuotientPairingCoreTarget : Prop :=
  ∀ {K : Type u} [Field K] [DecidableEq K] [NumberField K],
    ∀ (E : WeierstrassCurve K) [E.IsElliptic] (h : CanonicalHeightCore K E)
      (p : PolarizationCore K E h.canonicalHeight),
      Nonempty (QuotientPairingCore K E p.pairing)

/-- Checked composition of the three explicit semantic packages into the exact
canonical target.  All mathematical construction remains in the premises. -/
theorem root_of_height_polarization_quotient
    (heightCore : CanonicalHeightCoreTarget.{u})
    (polarizationCore : PolarizationCoreTarget.{u})
    (quotientCore : QuotientPairingCoreTarget.{u}) :
    NeronTatePairingTarget.{u} := by
  intro K _ _ _ E _
  let h := Classical.choice (heightCore E)
  let p := Classical.choice (polarizationCore E h)
  let q := Classical.choice (quotientCore E h p)
  exact ⟨{
    canonicalHeight := h.canonicalHeight
    limit_formula := h.limit_formula
    bounded_difference := h.bounded_difference
    pairing := p.pairing
    polarization := p.polarization
    symmetric := p.symmetric
    add_left := p.add_left
    add_right := p.add_right
    zsmul_left := p.zsmul_left
    zsmul_right := p.zsmul_right
    self_pairing := p.self_pairing
    diagonal_nonnegative := p.diagonal_nonnegative
    diagonal_kernel := p.diagonal_kernel
    quotientPairing := q.quotientPairing
    quotient_lift := q.quotient_lift
    quotient_positive_definite := q.quotient_positive_definite
  }⟩

#print axioms root_of_height_polarization_quotient

end Stage1Instances.THM_M_0452
