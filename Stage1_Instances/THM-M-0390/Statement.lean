import Init

/-!
# THM-M-0390: exact Catalan/Mihailescu statement boundary

This module freezes the proposition and statement-level transports only. It
does not assert the proposition.
-/

namespace Stage1.THM_M_0390

/-- A nontrivial perfect power in the positive natural-number encoding. -/
def NontrivialPower (n : Nat) : Prop :=
  exists base exponent : Nat, 1 < base /\ 1 < exponent /\ n = base ^ exponent

/-- The exact oriented exponential-equation target. -/
def CatalanStatement : Prop :=
  forall x p y q : Nat,
    1 < x -> 1 < p -> 1 < y -> 1 < q ->
    x ^ p + 1 = y ^ q ->
    x = 2 /\ p = 3 /\ y = 3 /\ q = 2

/-- The equivalent formulation in terms of consecutive perfect-power values. -/
def ConsecutivePowerStatement : Prop :=
  forall lower upper : Nat,
    lower + 1 = upper ->
    NontrivialPower lower ->
    NontrivialPower upper ->
    lower = 8 /\ upper = 9

/-- Checked transport from the exact tuple statement to the consecutive-value form. -/
theorem catalanStatement_implies_consecutivePowerStatement :
    CatalanStatement -> ConsecutivePowerStatement := by
  intro h lower upper hsucc hlower hupper
  rcases hlower with ⟨x, p, hx, hp, rfl⟩
  rcases hupper with ⟨y, q, hy, hq, rfl⟩
  have result := h x p y q hx hp hy hq hsucc
  rcases result with ⟨rfl, rfl, rfl, rfl⟩
  decide

/-- Exact-type fixture for binder order, hypotheses, and conclusion. -/
theorem catalanStatement_exact_type :
    CatalanStatement =
      (forall x p y q : Nat,
        1 < x -> 1 < p -> 1 < y -> 1 < q ->
        x ^ p + 1 = y ^ q ->
        x = 2 /\ p = 3 /\ y = 3 /\ q = 2) :=
  rfl

/-- Removed-hypothesis mutation used by the statement checker. -/
def MutationRemovedExponentBound : Prop :=
  forall x p y q : Nat,
    1 < x -> 1 < y -> 1 < q ->
    x ^ p + 1 = y ^ q ->
    x = 2 /\ p = 3 /\ y = 3 /\ q = 2

/-- Changing the carrier to integers changes the canonical target. -/
def MutationChangedDomain : Prop :=
  forall x p y q : Int,
    1 < x -> 1 < p -> 1 < y -> 1 < q ->
    x ^ p.natAbs + 1 = y ^ q.natAbs ->
    x = 2 /\ p = 3 /\ y = 3 /\ q = 2

/-- Moving the exponent binders under the base hypotheses changes binder scope. -/
def MutationChangedBinderScope : Prop :=
  forall x y : Nat, 1 < x -> 1 < y ->
    exists p q : Nat, 1 < p /\ 1 < q /\
      (x ^ p + 1 = y ^ q -> x = 2 /\ p = 3 /\ y = 3 /\ q = 2)

/-- Allowing the boundary exponent `p = 1` changes the claim. -/
def MutationExponentBoundary : Prop :=
  forall x p y q : Nat,
    1 < x -> 0 < p -> 1 < y -> 1 < q ->
    x ^ p + 1 = y ^ q ->
    x = 2 /\ p = 3 /\ y = 3 /\ q = 2

/-- The removed-`p` mutation is false at `9^1 + 1 = 10^1`? -/
theorem mutationRemovedExponentBound_is_false :
    Not MutationRemovedExponentBound := by
  intro h
  have bad := h 8 1 3 2 (by decide) (by decide) (by decide) (by decide)
  exact (by decide : (8 : Nat) ≠ 2) bad.1

/-- The weakened exponent boundary is false at `8^1 + 1 = 3^2`. -/
theorem mutationExponentBoundary_is_false :
    Not MutationExponentBoundary := by
  intro h
  have bad := h 8 1 3 2 (by decide) (by decide) (by decide) (by decide) (by decide)
  exact (by decide : (8 : Nat) ≠ 2) bad.1

#print CatalanStatement
#print MutationRemovedExponentBound
#print MutationChangedDomain
#print MutationChangedBinderScope
#print MutationExponentBoundary

end Stage1.THM_M_0390
