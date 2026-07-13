import Mathlib.Data.ZMod.Basic

/-!
# THM-M-0931: exact Erdos-Ginzburg-Ziv statement

This module freezes the positive, exact-count, occurrence-preserving integer
statement read from the 1961 source. It defines the target and checked statement
transports only; it does not import or prove the Erdos-Ginzburg-Ziv theorem.
-/

namespace Stage1Instances.THM_M_0931

/-- Among exactly `2 * n - 1` integer occurrences, for positive `n`, there are
exactly `n` selected occurrences whose sum is divisible by `n`. -/
def ErdosGinzburgZivTarget : Prop :=
  forall (n : Nat), 0 < n -> forall (s : Multiset Int),
    s.card = 2 * n - 1 ->
      exists t : Multiset Int, t <= s /\ t.card = n /\ (n : Int) ∣ t.sum

/-- The stronger input-cardinality shape exposed by the pinned mathlib theorem.
This declaration records only its proposition; no proof-bearing module is imported. -/
def AtLeastCountTarget : Prop :=
  forall (n : Nat) (s : Multiset Int),
    2 * n - 1 <= s.card ->
      exists t : Multiset Int, t <= s /\ t.card = n /\ (n : Int) ∣ t.sum

/-- The exact source target expressed by reduction of the selected integer sum
to `ZMod n`. The occurrence container and all binders are unchanged. -/
def ResidueTarget : Prop :=
  forall (n : Nat), 0 < n -> forall (s : Multiset Int),
    s.card = 2 * n - 1 ->
      exists t : Multiset Int, t <= s /\ t.card = n /\ (t.sum : ZMod n) = 0

/-- Checked equality-to-lower-bound specialization from the stronger proposition
shape to the exact source-shaped root. -/
theorem atLeastCountTarget_implies_erdosGinzburgZivTarget :
    AtLeastCountTarget -> ErdosGinzburgZivTarget := by
  intro h n _ s hs
  exact h n s hs.ge

/-- Checked divisibility-to-residue transport for the exact source-shaped root. -/
theorem erdosGinzburgZivTarget_iff_residueTarget :
    ErdosGinzburgZivTarget <-> ResidueTarget := by
  simp only [ErdosGinzburgZivTarget, ResidueTarget,
    ZMod.intCast_zmod_eq_zero_iff_dvd]

-- Structural mutations. Each elaborates but changes the frozen proposition.

/-- Removed-hypothesis mutation: the source's positive-modulus boundary is absent. -/
def mutationRemovedPositivity : Prop :=
  forall (n : Nat) (s : Multiset Int),
    s.card = 2 * n - 1 ->
      exists t : Multiset Int, t <= s /\ t.card = n /\ (n : Int) ∣ t.sum

/-- Changed-domain mutation: nonnegative naturals replace arbitrary integers. -/
def mutationNaturalInputs : Prop :=
  forall (n : Nat), 0 < n -> forall (s : Multiset Nat),
    s.card = 2 * n - 1 ->
      exists t : Multiset Nat, t <= s /\ t.card = n /\ n ∣ t.sum

/-- Changed-scope mutation: one favorable modulus is chosen existentially. -/
def mutationExistentialModulus : Prop :=
  exists n : Nat, 0 < n /\ forall (s : Multiset Int),
    s.card = 2 * n - 1 ->
      exists t : Multiset Int, t <= s /\ t.card = n /\ (n : Int) ∣ t.sum

/-- Boundary mutation: inputs larger than the source's exact count are admitted. -/
def mutationAtLeastInputCount : Prop :=
  forall (n : Nat), 0 < n -> forall (s : Multiset Int),
    2 * n - 1 <= s.card ->
      exists t : Multiset Int, t <= s /\ t.card = n /\ (n : Int) ∣ t.sum

#check_failure
  (rfl : ErdosGinzburgZivTarget = mutationRemovedPositivity)
#check_failure
  (rfl : ErdosGinzburgZivTarget = mutationNaturalInputs)
#check_failure
  (rfl : ErdosGinzburgZivTarget = mutationExistentialModulus)
#check_failure
  (rfl : ErdosGinzburgZivTarget = mutationAtLeastInputCount)

#print axioms Stage1Instances.THM_M_0931.atLeastCountTarget_implies_erdosGinzburgZivTarget
#print axioms Stage1Instances.THM_M_0931.erdosGinzburgZivTarget_iff_residueTarget

end Stage1Instances.THM_M_0931

set_option pp.explicit true in
set_option pp.universes true in
#print Stage1Instances.THM_M_0931.ErdosGinzburgZivTarget
