import Mathlib.NumberTheory.LucasLehmer

/-!
# THM-M-0484 canonical Lean statement

This module freezes the natural-exponent Lucas-Lehmer correctness criterion selected at intake.
The single direct import owns the recurrence and test vocabulary. This file checks statement
transports and boundary mutations only; it does not install proof credit for the canonical target.
-/

set_option autoImplicit false

namespace Stage1Instances.THM_M_0484

/-- For every exponent at least three, the Lucas-Lehmer test accepts exactly the prime Mersenne
numbers. -/
def LucasLehmerTestTarget : Prop :=
  forall p : Nat, 3 <= p ->
    (LucasLehmer.LucasLehmerTest p <-> Nat.Prime (mersenne p))

/-- The canonical target with the test predicate definition expanded to its `ZMod` residue. -/
def LucasLehmerResidueTarget : Prop :=
  forall p : Nat, 3 <= p ->
    (LucasLehmer.lucasLehmerResidue p = 0 <-> Nat.Prime (mersenne p))

/-- The canonical target expressed through the integer recurrence reduced at every step. -/
def LucasLehmerIntegerResidueTarget : Prop :=
  forall p : Nat, 3 <= p ->
    (LucasLehmer.sMod p (p - 2) = 0 <-> Nat.Prime (mersenne p))

/-- Expanding `LucasLehmerTest` preserves the exact target definitionally. -/
theorem lucasLehmerTestTarget_iff_residueTarget :
    LucasLehmerTestTarget <-> LucasLehmerResidueTarget := by
  rfl

/-- The library's checked `ZMod`/integer-residue bridge preserves the exact target. -/
theorem lucasLehmerTestTarget_iff_integerResidueTarget :
    LucasLehmerTestTarget <-> LucasLehmerIntegerResidueTarget := by
  constructor
  · intro h p hp
    exact (LucasLehmer.residue_eq_zero_iff_sMod_eq_zero p (by omega)).symm.trans (h p hp)
  · intro h p hp
    exact (LucasLehmer.residue_eq_zero_iff_sMod_eq_zero p (by omega)).trans (h p hp)

/-! Structural mutations elaborate as propositions but must not have the canonical target's type. -/

/-- Mutation: delete the lower-bound hypothesis. -/
def mutationRemovedLowerBound : Prop :=
  forall p : Nat,
    LucasLehmer.LucasLehmerTest p <-> Nat.Prime (mersenne p)

/-- Mutation: replace the all-natural domain above the bound by all prime exponents. -/
def mutationChangedDomainToPrimeExponent : Prop :=
  forall p : Nat, p.Prime ->
    (LucasLehmer.LucasLehmerTest p <-> Nat.Prime (mersenne p))

/-- Mutation: scope the lower bound over only the test side of the equivalence. -/
def mutationChangedLowerBoundScope : Prop :=
  forall p : Nat,
    (3 <= p -> LucasLehmer.LucasLehmerTest p) <-> Nat.Prime (mersenne p)

/-- Mutation: include the exceptional exponent two. -/
def mutationIncludedExponentTwo : Prop :=
  forall p : Nat, 2 <= p ->
    (LucasLehmer.LucasLehmerTest p <-> Nat.Prime (mersenne p))

variable
  (hRemoved : mutationRemovedLowerBound)
  (hDomain : mutationChangedDomainToPrimeExponent)
  (hScope : mutationChangedLowerBoundScope)
  (hBoundary : mutationIncludedExponentTwo)

#check_failure (show LucasLehmerTestTarget from hRemoved)
#check_failure (show LucasLehmerTestTarget from hDomain)
#check_failure (show LucasLehmerTestTarget from hScope)
#check_failure (show LucasLehmerTestTarget from hBoundary)

/-- At exponent two the Mersenne number is prime but the Lucas-Lehmer test is false. -/
theorem exponentTwo_boundary :
    Nat.Prime (mersenne 2) /\ Not (LucasLehmer.LucasLehmerTest 2) := by
  constructor
  · decide
  · norm_num

theorem mutationRemovedLowerBound_is_false : Not mutationRemovedLowerBound := by
  intro h
  exact exponentTwo_boundary.2 ((h 2).mpr exponentTwo_boundary.1)

theorem mutationChangedDomainToPrimeExponent_is_false :
    Not mutationChangedDomainToPrimeExponent := by
  intro h
  exact exponentTwo_boundary.2 ((h 2 Nat.prime_two).mpr exponentTwo_boundary.1)

theorem mutationChangedLowerBoundScope_is_false : Not mutationChangedLowerBoundScope := by
  intro h
  have hPrimeZero : Nat.Prime (mersenne 0) := (h 0).mp (by omega)
  exact Nat.not_prime_zero (by simpa [mersenne] using hPrimeZero)

theorem mutationIncludedExponentTwo_is_false : Not mutationIncludedExponentTwo := by
  intro h
  exact exponentTwo_boundary.2 ((h 2 (by omega)).mpr exponentTwo_boundary.1)

#check lucasLehmerTestTarget_iff_residueTarget
#check lucasLehmerTestTarget_iff_integerResidueTarget
#print axioms lucasLehmerTestTarget_iff_residueTarget
#print axioms lucasLehmerTestTarget_iff_integerResidueTarget

set_option pp.explicit true in
set_option pp.universes true in
#print LucasLehmerTestTarget

end Stage1Instances.THM_M_0484
