import Statement
import Mathlib.NumberTheory.Wilson

/-!
# THM-M-0476 conditional obligation composition

This module checks the child-to-parent interfaces frozen by the Wilson obligation registry. Every
mathematical engine remains an explicit premise: the file does not install `ZMod.wilsons_lemma`,
close the canonical root, or grant proof credit to the audited candidate.
-/

namespace Stage1Instances.THM_M_0476.ObligationTree

open Finset Nat
open scoped Nat

/-- The exact typeclass-premise interface exported by the audited Wilson candidate. -/
def FactWilsonAnchor : Prop :=
  forall (p : Nat) [Fact p.Prime], ((p - 1)! : ZMod p) = -1

/-- Cast the natural factorial identity to the interval product used in Wilson's proof. -/
def FactorialProductBridge : Prop :=
  forall (p : Nat) [Fact p.Prime],
    ((p - 1)! : ZMod p) =
      ∏ x ∈ Finset.Ico 1 ((p - 1) + 1), (x : ZMod p)

/-- The primitive natural interval-product identity. -/
def FactorialIntervalIdentity : Prop :=
  forall n : Nat, (∏ x ∈ Finset.Ico 1 (n + 1), x) = n !

/-- Casting a natural interval product commutes with the finite product. -/
def NatIntervalCastIdentity : Prop :=
  forall (p n : Nat),
    (((∏ x ∈ Finset.Ico 1 (n + 1), x) : Nat) : ZMod p) =
      ∏ x ∈ Finset.Ico 1 (n + 1), (x : ZMod p)

/-- Natural-subtraction endpoint normalization used by the residue bijection. -/
def PrimeEndpointIdentity : Prop :=
  forall (p : Nat) [Fact p.Prime],
    (p - 1) + 1 = p

/-- Replace the nonzero residue representatives by all units of `ZMod p`. -/
def ResidueUnitsProductBridge : Prop :=
  forall (p : Nat) [Fact p.Prime],
    (∏ x ∈ Finset.Ico 1 ((p - 1) + 1), (x : ZMod p)) =
      ∏ x : (ZMod p)ˣ, (x : ZMod p)

/-- Every unit representative is positive and below the prime modulus. -/
def UnitRepresentativeInPrimeRange : Prop :=
  forall (p : Nat) [Fact p.Prime] (a : (ZMod p)ˣ),
    1 <= (a : ZMod p).val /\ (a : ZMod p).val < p

/-- Unit representatives are injective. -/
def UnitRepresentativeInjective : Prop :=
  forall (p : Nat) [Fact p.Prime] (a b : (ZMod p)ˣ),
    (a : ZMod p).val = (b : ZMod p).val -> a = b

/-- Every positive representative below the modulus lifts to a unit. -/
def ResidueRepresentativeSurjectiveAtEndpoint : Prop :=
  forall (p : Nat) [Fact p.Prime] (b : Nat),
    1 <= b -> b < p ->
      exists a : (ZMod p)ˣ, (a : ZMod p).val = b

/-- Coercing a unit agrees with casting its canonical representative. -/
def RepresentativeCastAgreement : Prop :=
  forall (p : Nat) [Fact p.Prime] (a : (ZMod p)ˣ),
    (a : ZMod p) = ((a : ZMod p).val : ZMod p)

/-- The product of all units, as a unit, is negative one. -/
def UnitProductIdentity : Prop :=
  forall (p : Nat) [Fact p.Prime],
    (∏ x : (ZMod p)ˣ, x) = (-1 : (ZMod p)ˣ)

/-- The product away from negative one cancels by inverse pairing. -/
def UnitEraseNegOneProduct : Prop :=
  forall (p : Nat) [Fact p.Prime],
    (∏ x ∈ (Finset.univ.erase (-1 : (ZMod p)ˣ)), x) = 1

/-- In an integral-domain unit group, the inverse fixed points are exactly `1` and `-1`. -/
def InverseFixedPointClassification : Prop :=
  forall (p : Nat) [Fact p.Prime] (a : (ZMod p)ˣ),
    a⁻¹ = a <-> a = 1 \/ a = -1

/-- The all-units product, after coercion to `ZMod p`, is negative one. -/
def UnitsProductBridge : Prop :=
  forall (p : Nat) [Fact p.Prime],
    (∏ x : (ZMod p)ˣ, (x : ZMod p)) = -1

/-- Checked composition of the primitive factorial and cast identities. -/
theorem factorialProduct_of_identities
    (factorial : FactorialIntervalIdentity)
    (castProduct : NatIntervalCastIdentity) :
    FactorialProductBridge := by
  intro p _
  calc
    ((p - 1)! : ZMod p) =
        (((∏ x ∈ Finset.Ico 1 ((p - 1) + 1), x) : Nat) : ZMod p) := by
          exact congrArg (fun n : Nat => (n : ZMod p)) (factorial (p - 1)).symm
    _ = ∏ x ∈ Finset.Ico 1 ((p - 1) + 1), (x : ZMod p) :=
      castProduct p (p - 1)

/-- Checked `Finset.prod_bij` composition of all representative-to-unit obligations. -/
theorem residueUnitsProduct_of_components
    (endpoint : PrimeEndpointIdentity)
    (inPrimeRange : UnitRepresentativeInPrimeRange)
    (injective : UnitRepresentativeInjective)
    (surjectiveAtEndpoint : ResidueRepresentativeSurjectiveAtEndpoint)
    (castAgreement : RepresentativeCastAgreement) :
    ResidueUnitsProductBridge := by
  intro p _
  symm
  refine Finset.prod_bij (fun a _ => (a : ZMod p).val) ?_ ?_ ?_ ?_
  · intro a _
    rw [Finset.mem_Ico, endpoint p]
    exact inPrimeRange p a
  · intro a _ b _ hab
    exact injective p a b hab
  · intro b hb
    rw [Finset.mem_Ico, endpoint p] at hb
    obtain ⟨a, ha⟩ := surjectiveAtEndpoint p b hb.1 hb.2
    exact ⟨a, Finset.mem_univ a, ha⟩
  · intro a _
    exact castAgreement p a

/-- Checked endpoint normalization obtained from the prime premise. -/
theorem primeEndpointIdentity_from_prime : PrimeEndpointIdentity := by
  intro p hp
  exact Nat.sub_add_cancel hp.out.one_le

/-- Checked range bounds for the canonical representative of a unit. -/
theorem unitRepresentativeInPrimeRange_from_unit : UnitRepresentativeInPrimeRange := by
  intro p _ a
  constructor
  · apply Nat.pos_of_ne_zero
    rw [← @ZMod.val_zero p]
    intro h
    exact Units.ne_zero a (ZMod.val_injective p h)
  · exact ZMod.val_lt _

/-- Checked construction of a unit from a positive representative below the modulus. -/
theorem residueRepresentativeSurjectiveAtEndpoint_from_mk0 :
    ResidueRepresentativeSurjectiveAtEndpoint := by
  intro p _ b hbpos hblt
  refine ⟨Units.mk0 b ?_, ?_⟩
  · intro h
    have hval := congrArg ZMod.val h
    apply (Nat.ne_of_gt hbpos)
    simpa only [ZMod.val_cast_of_lt hblt, ZMod.val_zero] using hval
  · simp only [ZMod.val_cast_of_lt hblt, Units.val_mk0]

/-- Checked injectivity of unit representatives. -/
theorem unitRepresentativeInjective_from_val : UnitRepresentativeInjective := by
  intro p _ a b h
  rw [Units.ext_iff]
  exact ZMod.val_injective p h

/-- Checked agreement between a unit and the cast of its representative. -/
theorem representativeCastAgreement_from_natCast_val : RepresentativeCastAgreement := by
  intro p _ a
  calc
    (a : ZMod p) = ZMod.cast (a : ZMod p) := (ZMod.cast_id p _).symm
    _ = ((a : ZMod p).val : ZMod p) :=
      (@ZMod.natCast_val p (ZMod p) (ZMod.commRing p).toRing inferInstance _).symm

/-- Checked fixed-point classification used by inverse pairing. -/
theorem inverseFixedPointClassification_from_units : InverseFixedPointClassification := by
  intro p _ a
  exact Units.inv_eq_self_iff (R := ZMod p) a

/-- Checked inverse-pairing composition over all units except negative one. -/
theorem unitEraseProduct_of_inversion
    (fixedPoints : InverseFixedPointClassification) :
    UnitEraseNegOneProduct := by
  intro p _
  classical
  refine Finset.prod_involution
    (s := Finset.univ.erase (-1 : (ZMod p)ˣ))
    (f := fun x : (ZMod p)ˣ => x)
    (fun a _ => a⁻¹) ?_ ?_ ?_ ?_
  · intro a ha
    exact mul_inv_cancel a
  · intro a ha haOne hfixed
    rcases (fixedPoints p a).mp hfixed with hOne | hNeg
    · exact haOne hOne
    · exact (Finset.ne_of_mem_erase ha) hNeg
  · intro a ha
    rw [Finset.mem_erase] at ha
    apply Finset.mem_erase.mpr
    exact And.intro (fun h => ha.1 (inv_injective h)) (Finset.mem_univ _)
  · intro a ha
    exact inv_inv a

/-- Checked insertion of negative one into the inverse-paired product. -/
theorem unitProductIdentity_of_erase
    (eraseProduct : UnitEraseNegOneProduct) : UnitProductIdentity := by
  intro p _
  rw [← Finset.insert_erase (Finset.mem_univ (-1 : (ZMod p)ˣ))]
  rw [Finset.prod_insert (Finset.notMem_erase (-1 : (ZMod p)ˣ) Finset.univ)]
  rw [eraseProduct p, mul_one]

/-- Checked coercion of the unit-valued product identity into `ZMod p`. -/
theorem unitsProductBridge_of_components
    (unitProduct : UnitProductIdentity) : UnitsProductBridge := by
  intro p _
  calc
    (∏ x : (ZMod p)ˣ, (x : ZMod p)) =
        ((↑(∏ x : (ZMod p)ˣ, x) : ZMod p)) :=
      by
        simpa only [Units.coeHom_apply] using
          (map_prod (Units.coeHom (ZMod p))
            (fun x : (ZMod p)ˣ => x) Finset.univ).symm
    _ = ((↑(-1 : (ZMod p)ˣ) : ZMod p)) :=
      congrArg (fun u : (ZMod p)ˣ => (u : ZMod p)) (unitProduct p)
    _ = -1 := by simp only [Units.val_neg, Units.val_one]

/-- Checked composition of the three exact mathematical bridges into the audited Fact interface. -/
theorem factWilsonAnchor_of_bridges
    (factorialProduct : FactorialProductBridge)
    (residueUnits : ResidueUnitsProductBridge)
    (unitsProduct : UnitsProductBridge) : FactWilsonAnchor := by
  intro p _
  calc
    ((p - 1)! : ZMod p) =
        ∏ x ∈ Finset.Ico 1 ((p - 1) + 1), (x : ZMod p) := factorialProduct p
    _ = ∏ x : (ZMod p)ˣ, (x : ZMod p) := residueUnits p
    _ = -1 := unitsProduct p

/-- Checked explicit-prime-to-`Fact` transport into the exact canonical root. -/
theorem root_of_factWilsonAnchor
    (anchor : FactWilsonAnchor) :
    Stage1Instances.THM_M_0476.WilsonTheoremTarget := by
  intro p hp
  letI : Fact p.Prime := ⟨hp⟩
  exact anchor p

/-- The final parent identity keeps the graph root distinct from its terminal composition node. -/
theorem root_of_composedTarget
    (target : Stage1Instances.THM_M_0476.WilsonTheoremTarget) :
    Stage1Instances.THM_M_0476.WilsonTheoremTarget := target

#check Finset.prod_Ico_id_eq_factorial
#check Finset.prod_natCast
#check Finset.prod_bij
#check Finset.prod_involution
#check Units.inv_eq_self_iff
#check FiniteField.prod_univ_units_id_eq_neg_one
#check ZMod.wilsons_lemma
#print axioms factorialProduct_of_identities
#print axioms primeEndpointIdentity_from_prime
#print axioms residueUnitsProduct_of_components
#print axioms unitRepresentativeInPrimeRange_from_unit
#print axioms residueRepresentativeSurjectiveAtEndpoint_from_mk0
#print axioms unitRepresentativeInjective_from_val
#print axioms representativeCastAgreement_from_natCast_val
#print axioms inverseFixedPointClassification_from_units
#print axioms unitEraseProduct_of_inversion
#print axioms unitProductIdentity_of_erase
#print axioms unitsProductBridge_of_components
#print axioms factWilsonAnchor_of_bridges
#print axioms root_of_factWilsonAnchor
#print axioms root_of_composedTarget

set_option pp.universes true in
set_option pp.explicit true in
#print Stage1Instances.THM_M_0476.WilsonTheoremTarget

end Stage1Instances.THM_M_0476.ObligationTree
