import Mathlib.Data.Nat.Factorial.Basic
import Mathlib.Data.Nat.Prime.Defs
import Mathlib.Data.ZMod.Defs

/-!
# THM-M-0476 canonical Lean statement

This module freezes the conventional forward, natural-prime formulation of Wilson's theorem
selected from the repository catalog. It imports only primitive statement vocabulary and contains
no proof of the canonical target.
-/

open scoped Nat

namespace Stage1Instances.THM_M_0476

/-- For every natural prime `p`, the factorial of `p - 1`, cast to `ZMod p`, is `-1`. -/
def WilsonTheoremTarget : Prop :=
  forall (p : Nat), p.Prime -> ((p - 1)! : ZMod p) = -1

/-- The same target with the prime premise represented by a `Fact` instance. -/
def WilsonTheoremFactTarget : Prop :=
  forall (p : Nat) [Fact p.Prime], ((p - 1)! : ZMod p) = -1

/-- Checked transport between the explicit and typeclass prime-premise encodings. -/
theorem wilsonTheoremTarget_iff_factTarget :
    WilsonTheoremTarget <-> WilsonTheoremFactTarget := by
  constructor
  · intro h p
    exact h p Fact.out
  · intro h p hp
    letI : Fact p.Prime := ⟨hp⟩
    exact h p

/-! Structural mutations elaborate as propositions but must not equal the canonical target. -/

/-- Removed-hypothesis mutation: assert the congruence for every natural modulus. -/
def mutationRemovedPrimeHypothesis : Prop :=
  forall (p : Nat), ((p - 1)! : ZMod p) = -1

/-- Changed-domain mutation: specialize the modulus to natural numbers represented by `UInt64`. -/
def mutationChangedDomainToUInt64 : Prop :=
  forall (p : UInt64), p.toNat.Prime ->
    ((p.toNat - 1)! : ZMod p.toNat) = -1

/-- Changed-scope mutation: replace the universal prime modulus by one existential witness. -/
def mutationChangedPrimeBinderScope : Prop :=
  exists p : Nat, p.Prime /\ ((p - 1)! : ZMod p) = -1

/-- Boundary mutation: wrongly extend the target to the composite modulus four. -/
def mutationIncludedCompositeFour : Prop :=
  forall (p : Nat), (p.Prime \/ p = 4) -> ((p - 1)! : ZMod p) = -1

/-- The added composite boundary makes the mutation false. -/
theorem mutationIncludedCompositeFour_false : Not mutationIncludedCompositeFour := by
  intro h
  have hFour : ((4 - 1)! : ZMod 4) = -1 := h 4 (Or.inr rfl)
  have hCounterexample : Not (((4 - 1)! : ZMod 4) = -1) := by decide
  exact hCounterexample hFour

variable
  (hRemoved : mutationRemovedPrimeHypothesis)
  (hDomain : mutationChangedDomainToUInt64)
  (hScope : mutationChangedPrimeBinderScope)
  (hBoundary : mutationIncludedCompositeFour)

#check_failure (show WilsonTheoremTarget from hRemoved)
#check_failure (show WilsonTheoremTarget from hDomain)
#check_failure (show WilsonTheoremTarget from hScope)
#check_failure (show WilsonTheoremTarget from hBoundary)

#check wilsonTheoremTarget_iff_factTarget
#check mutationIncludedCompositeFour_false
#print axioms wilsonTheoremTarget_iff_factTarget
#print axioms mutationIncludedCompositeFour_false

set_option pp.explicit true in
set_option pp.universes true in
#print WilsonTheoremTarget

end Stage1Instances.THM_M_0476
