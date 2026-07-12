import ObligationTree
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0474 proof execution

This module installs the exact, manifest-pinned mathlib proof body at the frozen natural-number
target. The direct wrapper and the wrapper through the frozen composition interface are separate
exact-type checks; they share one upstream terminal proof body and do not receive duplicate proof
credit.
-/

namespace Stage1Instances.THM_M_0474.Proof

open Stage1Instances.THM_M_0474

/-! Exact interfaces for the semantic children in the frozen proof graph. -/

universe u

def NatIntNormalization : Prop :=
  forall (p a : Nat),
    (a : Int) ^ (p - 1) ≡ 1 [ZMOD p] ->
      a ^ (p - 1) ≡ 1 [MOD p]

def CoprimeNormalization : Prop :=
  forall (p a : Nat), a.Coprime p -> IsCoprime (a : Int) (p : Int)

def IntegerFermatAnchor : Prop :=
  forall (p : Nat) (n : Int), p.Prime -> IsCoprime n (p : Int) ->
    n ^ (p - 1) ≡ 1 [ZMOD p]

def ZModNonzeroConstruction : Prop :=
  forall (p : Nat) (n : Int), p.Prime -> IsCoprime n (p : Int) ->
    (n : ZMod p) ≠ 0

def IntZModTransport : Prop :=
  forall (p : Nat) (n : Int),
    (n : ZMod p) ^ (p - 1) = 1 -> n ^ (p - 1) ≡ 1 [ZMOD p]

def ZModFermatAnchor : Prop :=
  forall (p : Nat), p.Prime -> forall a : ZMod p, a ≠ 0 -> a ^ (p - 1) = 1

def ZModCardTransport : Prop :=
  forall (p : Nat) [Fact p.Prime] (a : ZMod p),
    a ^ (Fintype.card (ZMod p) - 1) = 1 -> a ^ (p - 1) = 1

def FiniteFieldAnchor : Prop :=
  forall (K : Type u) [GroupWithZero K] [Fintype K] (a : K),
    a ≠ 0 -> a ^ (Fintype.card K - 1) = 1

def UnitConstruction : Prop :=
  forall (K : Type u) [GroupWithZero K] [Fintype K]
    (a : K) (ha : a ≠ 0),
    a ^ (Fintype.card K - 1) =
      ((Units.mk0 a ha ^ (Fintype.card K - 1) : Kˣ) : K)

def GroupCardAnchor : Prop :=
  forall (G : Type u) [Group G] [Fintype G] (x : G), x ^ Fintype.card G = 1

/-- Natural-to-integer congruence normalization (`M0474-N-NAT-INT`). -/
theorem natIntNormalization : NatIntNormalization := by
  intro p a h
  rw [← Int.natCast_modEq_iff, Nat.cast_pow, Nat.cast_one]
  exact h

/-- Natural coprimality to integer `IsCoprime` normalization (`M0474-N-COPRIME`). -/
theorem coprimeNormalization : CoprimeNormalization := by
  intro p a ha
  exact Nat.isCoprime_iff_coprime.mpr ha

/-- The pinned integer Fermat bridge (`M0474-L-INT`). -/
theorem integerFermatAnchor : IntegerFermatAnchor := by
  intro p n hp hn
  exact Int.ModEq.pow_card_sub_one_eq_one hp hn

/-- Coprimality makes the integer residue nonzero in `ZMod p` (`M0474-C-ZMOD-NONZERO`). -/
theorem zModNonzeroConstruction : ZModNonzeroConstruction := by
  intro p n hp hn
  letI : Fact p.Prime := ⟨hp⟩
  intro hz
  have hdvd : (p : Int) ∣ n := (CharP.intCast_eq_zero_iff (ZMod p) p n).mp hz
  exact ((Nat.prime_iff_prime_int.mp hp).coprime_iff_not_dvd.mp hn.symm) hdvd

/-- Equality in `ZMod p` transports to integer congruence (`M0474-T-INT-ZMOD`). -/
theorem intZModTransport : IntZModTransport := by
  intro p n h
  simpa [← ZMod.intCast_eq_intCast_iff] using h

/-- The pinned `ZMod` finite-field bridge (`M0474-L-ZMOD`). -/
theorem zModFermatAnchor : ZModFermatAnchor := by
  intro p hp a ha
  letI : Fact p.Prime := ⟨hp⟩
  exact ZMod.pow_card_sub_one_eq_one ha

/-- Rewrite the finite cardinal of `ZMod p` to `p` (`M0474-T-ZMOD-CARD`). -/
theorem zModCardTransport : ZModCardTransport := by
  intro p _ a h
  simpa only [ZMod.card] using h

/-- The pinned finite group-with-zero bridge (`M0474-L-FINITE-FIELD`). -/
theorem finiteFieldAnchor : FiniteFieldAnchor.{u} := by
  intro K _ _ a ha
  exact FiniteField.pow_card_sub_one_eq_one a ha

/-- Construct the unit and identify its cardinal exponent (`M0474-C-UNIT`). -/
theorem unitConstruction : UnitConstruction.{u} := by
  intro K _ _ a ha
  rw [Units.val_pow_eq_pow_val, Units.val_mk0]

/-- Every element of a finite group has cardinal power one (`M0474-L-GROUP-CARD`). -/
theorem groupCardAnchor : GroupCardAnchor.{u} := by
  intro G _ _ x
  exact pow_card_eq_one

/-! Checked child-to-parent composition certificates for every nonleaf in the proof graph. -/

theorem finiteFieldAnchor_of_components
    (unit : UnitConstruction.{u}) (group : GroupCardAnchor.{u}) : FiniteFieldAnchor.{u} := by
  intro K _ _ a ha
  calc
    a ^ (Fintype.card K - 1) =
        ((Units.mk0 a ha ^ (Fintype.card K - 1) : Kˣ) : K) :=
      unit _ a ha
    _ = 1 := by
      classical
      have hgroup :
          (((Units.mk0 a ha ^ Fintype.card Kˣ : Kˣ)) : K) = 1 :=
        congrArg (fun u : Kˣ => (u : K)) (group Kˣ (Units.mk0 a ha))
      rwa [Fintype.card_units] at hgroup

theorem zModFermatAnchor_of_components
    (card : ZModCardTransport) (finiteField : FiniteFieldAnchor.{0}) : ZModFermatAnchor := by
  intro p hp a ha
  letI : Fact p.Prime := ⟨hp⟩
  exact card p a (finiteField _ a ha)

theorem integerFermatAnchor_of_components
    (nonzero : ZModNonzeroConstruction)
    (transport : IntZModTransport)
    (zmod : ZModFermatAnchor) : IntegerFermatAnchor := by
  intro p n hp hn
  exact transport p n (zmod p hp (n : ZMod p) (nonzero p n hp hn))

theorem exactNatAnchor_of_components
    (natInt : NatIntNormalization)
    (coprime : CoprimeNormalization)
    (integer : IntegerFermatAnchor) : ObligationTree.ExactNatAnchor := by
  intro p a hp ha
  exact natInt p a (integer p a hp (coprime p a ha))

/-- Exact canonical root wrapper over the pinned mathlib Fermat theorem. -/
theorem fermatLittleTheorem : FermatLittleTheoremTarget := by
  intro p a hp ha
  exact Nat.ModEq.pow_card_sub_one_eq_one hp ha

/-- Exact child required by the frozen composition interface. -/
theorem exactNatAnchor : ObligationTree.ExactNatAnchor := by
  intro p a hp ha
  exact Nat.ModEq.pow_card_sub_one_eq_one hp ha

/-- The same root checked through the frozen child-to-parent composition certificate. -/
theorem fermatLittleTheorem_via_frozen_composition : FermatLittleTheoremTarget :=
  ObligationTree.root_of_exactNatAnchor <|
    exactNatAnchor_of_components natIntNormalization coprimeNormalization <|
      integerFermatAnchor_of_components zModNonzeroConstruction intZModTransport <|
        zModFermatAnchor_of_components zModCardTransport <|
          finiteFieldAnchor_of_components unitConstruction groupCardAnchor

assert_no_sorry Nat.ModEq.pow_card_sub_one_eq_one
assert_no_sorry natIntNormalization
assert_no_sorry coprimeNormalization
assert_no_sorry integerFermatAnchor
assert_no_sorry zModNonzeroConstruction
assert_no_sorry intZModTransport
assert_no_sorry zModFermatAnchor
assert_no_sorry zModCardTransport
assert_no_sorry finiteFieldAnchor
assert_no_sorry unitConstruction
assert_no_sorry groupCardAnchor
assert_no_sorry finiteFieldAnchor_of_components
assert_no_sorry zModFermatAnchor_of_components
assert_no_sorry integerFermatAnchor_of_components
assert_no_sorry exactNatAnchor_of_components
assert_no_sorry fermatLittleTheorem
assert_no_sorry exactNatAnchor
assert_no_sorry fermatLittleTheorem_via_frozen_composition

#print sorries Nat.ModEq.pow_card_sub_one_eq_one
#print sorries natIntNormalization
#print sorries coprimeNormalization
#print sorries integerFermatAnchor
#print sorries zModNonzeroConstruction
#print sorries intZModTransport
#print sorries zModFermatAnchor
#print sorries zModCardTransport
#print sorries finiteFieldAnchor
#print sorries unitConstruction
#print sorries groupCardAnchor
#print sorries finiteFieldAnchor_of_components
#print sorries zModFermatAnchor_of_components
#print sorries integerFermatAnchor_of_components
#print sorries exactNatAnchor_of_components
#print sorries fermatLittleTheorem
#print sorries exactNatAnchor
#print sorries fermatLittleTheorem_via_frozen_composition

#print axioms Nat.ModEq.pow_card_sub_one_eq_one
#print axioms natIntNormalization
#print axioms coprimeNormalization
#print axioms integerFermatAnchor
#print axioms zModNonzeroConstruction
#print axioms intZModTransport
#print axioms zModFermatAnchor
#print axioms zModCardTransport
#print axioms finiteFieldAnchor
#print axioms unitConstruction
#print axioms groupCardAnchor
#print axioms finiteFieldAnchor_of_components
#print axioms zModFermatAnchor_of_components
#print axioms integerFermatAnchor_of_components
#print axioms exactNatAnchor_of_components
#print axioms fermatLittleTheorem
#print axioms exactNatAnchor
#print axioms fermatLittleTheorem_via_frozen_composition

end Stage1Instances.THM_M_0474.Proof
