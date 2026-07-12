import Mathlib.Data.Nat.ModEq
import Mathlib.Data.Nat.Prime.Defs

/-!
# THM-M-0474 canonical Lean statement

This module freezes the natural-number, coprime-base formulation of Fermat's little theorem
selected by the intake. It imports only the two primitive modules needed to state the target; the
proof-bearing finite-field module is deliberately not imported.
-/

namespace Stage1Instances.THM_M_0474

/-- If `p` is prime and `a` is coprime to `p`, then `a^(p - 1)` is one modulo `p`. -/
def FermatLittleTheoremTarget : Prop :=
  forall (p a : Nat), p.Prime -> a.Coprime p ->
    a ^ (p - 1) ≡ 1 [MOD p]

/-- The same natural-number target with nondivisibility in place of coprimality. -/
def FermatLittleTheoremNotDvdTarget : Prop :=
  forall (p a : Nat), p.Prime -> Not (p ∣ a) ->
    a ^ (p - 1) ≡ 1 [MOD p]

/-- Checked transport between the two accepted premise encodings. -/
theorem fermatLittleTheoremTarget_iff_notDvd :
    FermatLittleTheoremTarget ↔ FermatLittleTheoremNotDvdTarget := by
  constructor
  · intro h p a hp ha
    exact h p a hp (hp.coprime_iff_not_dvd.mpr ha).symm
  · intro h p a hp ha
    exact h p a hp (hp.coprime_iff_not_dvd.mp ha.symm)

/-! Structural mutations elaborate as propositions but must not have the canonical target's type. -/

def mutationRemovedCoprimeHypothesis : Prop :=
  forall (p a : Nat), p.Prime ->
    a ^ (p - 1) ≡ 1 [MOD p]

def mutationChangedDomainToIntegerModEq : Prop :=
  forall (p : Int) (a : Int), p.natAbs.Prime -> a.natAbs.Coprime p.natAbs ->
    p ∣ a ^ (p.natAbs - 1) - 1

def mutationChangedBaseBinderScope : Prop :=
  forall p : Nat, p.Prime ->
    exists a : Nat, a.Coprime p ∧ a ^ (p - 1) ≡ 1 [MOD p]

def mutationExcludedPrimeTwo : Prop :=
  forall (p a : Nat), p.Prime -> p ≠ 2 -> a.Coprime p ->
    a ^ (p - 1) ≡ 1 [MOD p]

variable
  (hRemoved : mutationRemovedCoprimeHypothesis)
  (hDomain : mutationChangedDomainToIntegerModEq)
  (hScope : mutationChangedBaseBinderScope)
  (hBoundary : mutationExcludedPrimeTwo)

#check_failure (show FermatLittleTheoremTarget from hRemoved)
#check_failure (show FermatLittleTheoremTarget from hDomain)
#check_failure (show FermatLittleTheoremTarget from hScope)
#check_failure (show FermatLittleTheoremTarget from hBoundary)

#check fermatLittleTheoremTarget_iff_notDvd
#print axioms fermatLittleTheoremTarget_iff_notDvd

set_option pp.explicit true in
set_option pp.universes true in
#print FermatLittleTheoremTarget

end Stage1Instances.THM_M_0474
