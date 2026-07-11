import Init

/-!
# THM-M-0390 obligation-tree composition surface

This module checks only the logical decomposition of the frozen Catalan target.
The three branch propositions are obligations, not asserted theorems.  In
particular, this file contains no proof of any branch and no proof of Catalan's
theorem.
-/

namespace Stage1.THM_M_0390

/-- The exact target, repeated definitionally so this standalone narrow check needs only `Init`. -/
def ObligationTreeRoot : Prop :=
  forall x p y q : Nat,
    1 < x -> 1 < p -> 1 < y -> 1 < q ->
    x ^ p + 1 = y ^ q ->
    x = 2 /\ p = 3 /\ y = 3 /\ q = 2

/-- Checked identity between the tree root and the statement module's target expression. -/
theorem obligationTreeRoot_exact_type :
    ObligationTreeRoot =
      (forall x p y q : Nat,
        1 < x -> 1 < p -> 1 < y -> 1 < q ->
        x ^ p + 1 = y ^ q ->
        x = 2 /\ p = 3 /\ y = 3 /\ q = 2) :=
  rfl

/-- The branch in which the exponent on the larger power is exactly two. -/
def BranchQEqTwo : Prop :=
  forall x p y q : Nat,
    1 < x -> 1 < p -> 1 < y -> 1 < q ->
    x ^ p + 1 = y ^ q -> q = 2 ->
    x = 2 /\ p = 3 /\ y = 3 /\ q = 2

/-- The branch with `q != 2` and exponent two on the smaller power. -/
def BranchQNeTwoPEqTwo : Prop :=
  forall x p y q : Nat,
    1 < x -> 1 < p -> 1 < y -> 1 < q ->
    x ^ p + 1 = y ^ q -> Not (q = 2) -> p = 2 ->
    x = 2 /\ p = 3 /\ y = 3 /\ q = 2

/-- The residual branch in which neither exponent is two. -/
def BranchNeitherExponentTwo : Prop :=
  forall x p y q : Nat,
    1 < x -> 1 < p -> 1 < y -> 1 < q ->
    x ^ p + 1 = y ^ q -> Not (q = 2) -> Not (p = 2) ->
    x = 2 /\ p = 3 /\ y = 3 /\ q = 2

/--
Checked exhaustiveness and recomposition certificate for the three exponent
branches.  Its arguments make the still-open mathematical premises explicit.
-/
theorem exponentBranches_compose
    (hq2 : BranchQEqTwo)
    (hqp2 : BranchQNeTwoPEqTwo)
    (hneither : BranchNeitherExponentTwo) :
    ObligationTreeRoot := by
  intro x p y q hx hp hy hq heq
  by_cases q2 : q = 2
  · exact hq2 x p y q hx hp hy hq heq q2
  · by_cases p2 : p = 2
    · exact hqp2 x p y q hx hp hy hq heq q2 p2
    · exact hneither x p y q hx hp hy hq heq q2 p2

/-- Exact-type fixture binding the composition certificate to the frozen root. -/
theorem exponentBranches_compose_exact_type :
    (BranchQEqTwo -> BranchQNeTwoPEqTwo ->
      BranchNeitherExponentTwo -> ObligationTreeRoot) =
    (BranchQEqTwo -> BranchQNeTwoPEqTwo ->
      BranchNeitherExponentTwo -> ObligationTreeRoot) :=
  rfl

#print BranchQEqTwo
#print BranchQNeTwoPEqTwo
#print BranchNeitherExponentTwo
#print exponentBranches_compose

end Stage1.THM_M_0390
