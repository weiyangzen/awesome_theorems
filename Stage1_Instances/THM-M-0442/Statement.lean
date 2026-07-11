import Mathlib.AlgebraicGeometry.EllipticCurve.Affine.Point
import Mathlib.GroupTheory.Torsion

/-!
# THM-M-0442 exact statement boundary

This module freezes Mazur's rational torsion classification as a proposition. It
contains statement transports and boundary checks, but no proof of the
classification.
-/

noncomputable section

open scoped WeierstrassCurve.Affine

namespace Stage1Instances.THMM0442

/-- The cyclic orders in Mazur's classification. -/
def IsMazurCyclicOrder (n : Nat) : Prop :=
  (1 <= n ∧ n <= 10) ∨ n = 12

/-- The parameter in the noncyclic family `Z/2Z x Z/(2*m)Z`. -/
def IsMazurBicyclicIndex (m : Nat) : Prop :=
  1 <= m ∧ m <= 4

/-- The historical parameterization by the order of the second cyclic factor. -/
def IsLegacySecondOrder (n : Nat) : Prop :=
  n = 2 ∨ n = 4 ∨ n = 6 ∨ n = 8

/-- The additive torsion subgroup of the rational points of `E`. -/
abbrev RationalTorsionGroup (E : WeierstrassCurve Rat) [E.IsElliptic] : Type :=
  AddCommGroup.torsion E⟮Rat⟯

def HasCyclicTorsionOrder
    (E : WeierstrassCurve Rat) [E.IsElliptic] (n : Nat) : Prop :=
  Nonempty (RationalTorsionGroup E ≃+ ZMod n)

def HasBicyclicTorsionIndex
    (E : WeierstrassCurve Rat) [E.IsElliptic] (m : Nat) : Prop :=
  Nonempty (RationalTorsionGroup E ≃+ (ZMod 2 × ZMod (2 * m)))

/-- The exact intake-selected necessity direction of Mazur's theorem. -/
def MazurRationalTorsionTarget : Prop :=
  ∀ (E : WeierstrassCurve Rat) [E.IsElliptic],
    (∃ n : Nat, IsMazurCyclicOrder n ∧ HasCyclicTorsionOrder E n) ∨
      (∃ m : Nat, IsMazurBicyclicIndex m ∧ HasBicyclicTorsionIndex E m)

/-- A local restatement of the historical candidate's `{2,4,6,8}` encoding. -/
def HistoricalCandidateShape : Prop :=
  ∀ (E : WeierstrassCurve Rat) [E.IsElliptic],
    (∃ n : Nat, IsMazurCyclicOrder n ∧ HasCyclicTorsionOrder E n) ∨
      (∃ n : Nat, IsLegacySecondOrder n ∧
        Nonempty (RationalTorsionGroup E ≃+ (ZMod 2 × ZMod n)))

theorem legacy_second_order_iff :
    IsLegacySecondOrder n ↔ ∃ m : Nat, IsMazurBicyclicIndex m ∧ n = 2 * m := by
  constructor
  · intro h
    rcases h with rfl | rfl | rfl | rfl
    · exact ⟨1, by simp [IsMazurBicyclicIndex], rfl⟩
    · exact ⟨2, by simp [IsMazurBicyclicIndex], rfl⟩
    · exact ⟨3, by simp [IsMazurBicyclicIndex], rfl⟩
    · exact ⟨4, by simp [IsMazurBicyclicIndex], rfl⟩
  · rintro ⟨m, hm, rfl⟩
    rcases hm with ⟨hm1, hm4⟩
    simp only [IsLegacySecondOrder]
    omega

/-- Checked transport from the intake parameterization to the historical one. -/
theorem mazurRationalTorsionTarget_iff_historicalCandidateShape :
    MazurRationalTorsionTarget ↔ HistoricalCandidateShape := by
  constructor
  · intro h E hE
    rcases h E with hcyclic | ⟨m, hm, htype⟩
    · exact Or.inl hcyclic
    · exact Or.inr ⟨2 * m, (legacy_second_order_iff.mpr ⟨m, hm, rfl⟩), htype⟩
  · intro h E hE
    rcases h E with hcyclic | ⟨n, hn, htype⟩
    · exact Or.inl hcyclic
    · rcases legacy_second_order_iff.mp hn with ⟨m, hm, rfl⟩
      exact Or.inr ⟨m, hm, htype⟩

-- Separately elaborated structural mutations inspected by `check_statement.py`.
def mutationOmitOrderTwelve : Prop :=
  ∀ (E : WeierstrassCurve Rat) [E.IsElliptic],
    (∃ n : Nat, 1 <= n ∧ n <= 10 ∧ HasCyclicTorsionOrder E n) ∨
      (∃ m : Nat, IsMazurBicyclicIndex m ∧ HasBicyclicTorsionIndex E m)

def mutationAdmitZeroBicyclicIndex : Prop :=
  ∀ (E : WeierstrassCurve Rat) [E.IsElliptic],
    (∃ n : Nat, IsMazurCyclicOrder n ∧ HasCyclicTorsionOrder E n) ∨
      (∃ m : Nat, m <= 4 ∧ HasBicyclicTorsionIndex E m)

def mutationExistentialCurve : Prop :=
  ∃ (E : WeierstrassCurve Rat) (_hE : E.IsElliptic),
    (∃ n : Nat, IsMazurCyclicOrder n ∧ HasCyclicTorsionOrder E n) ∨
      (∃ m : Nat, IsMazurBicyclicIndex m ∧ HasBicyclicTorsionIndex E m)

def mutationAddRealizabilityConverse : Prop :=
  MazurRationalTorsionTarget ∧
    ∀ n : Nat, IsMazurCyclicOrder n →
      ∃ (E : WeierstrassCurve Rat) (_hE : E.IsElliptic),
        HasCyclicTorsionOrder E n

/-- The lower and upper endpoints of the cyclic list are admitted. -/
theorem cyclic_endpoint_boundaries :
    IsMazurCyclicOrder 1 ∧ IsMazurCyclicOrder 10 ∧ IsMazurCyclicOrder 12 := by
  simp [IsMazurCyclicOrder]

/-- The noncyclic index endpoints correspond to second-factor orders 2 and 8. -/
theorem bicyclic_endpoint_boundaries :
    IsMazurBicyclicIndex 1 ∧ IsMazurBicyclicIndex 4 ∧
      IsLegacySecondOrder (2 * 1) ∧ IsLegacySecondOrder (2 * 4) := by
  simp [IsMazurBicyclicIndex, IsLegacySecondOrder]

end Stage1Instances.THMM0442

set_option pp.explicit true in
#print Stage1Instances.THMM0442.MazurRationalTorsionTarget
