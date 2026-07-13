import Mathlib.Data.Nat.Choose.Basic

/-!
# THM-M-0912: Pascal's identity statement

This module freezes the constrained predecessor form printed by NIST DLMF
26.3.5. The hypotheses preserve the displayed domain `m >= n >= 1`; the
broader zero-extended recurrence on all natural indices is not the target.
-/

namespace Stage1Instances.THM_M_0912

/-- The exact DLMF 26.3.5 predecessor recurrence, with its binders and
hypotheses made explicit. -/
def PascalIdentityTarget : Prop :=
  forall (m n : Nat), n <= m -> 1 <= n ->
    Nat.choose m n =
      Nat.choose (m - 1) n + Nat.choose (m - 1) (n - 1)

/-- The same source constraint represented as one conjunction. -/
def DLMFConjunctionTarget : Prop :=
  forall (m n : Nat), n <= m /\ 1 <= n ->
    Nat.choose m n =
      Nat.choose (m - 1) n + Nat.choose (m - 1) (n - 1)

/-- The same restricted recurrence with the summands in the order used by
`Nat.choose_eq_choose_pred_add`. This remains constrained to the source
domain and is not the all-natural successor recurrence. -/
def MathlibSummandOrderTarget : Prop :=
  forall (m n : Nat), n <= m -> 1 <= n ->
    Nat.choose m n =
      Nat.choose (m - 1) (n - 1) + Nat.choose (m - 1) n

/-- A domain-preserving successor reindexing. The `k <= r` premise is
essential: without it this would be broader than the DLMF statement. -/
def RestrictedSuccessorTarget : Prop :=
  forall (r k : Nat), k <= r ->
    Nat.choose (r + 1) (k + 1) =
      Nat.choose r (k + 1) + Nat.choose r k

/-- Checked transport between the curried Lean target and the conjunction
used to record the source's `m >= n >= 1` constraint. -/
theorem pascalIdentityTarget_iff_dlmfConjunctionTarget :
    PascalIdentityTarget <-> DLMFConjunctionTarget := by
  constructor
  · intro h m n hmn
    exact h m n hmn.1 hmn.2
  · intro h m n hnm hn
    exact h m n ⟨hnm, hn⟩

/-- Checked transport across the summand-order difference between DLMF and
the pinned mathlib predecessor lemma. -/
theorem pascalIdentityTarget_iff_mathlibSummandOrderTarget :
    PascalIdentityTarget <-> MathlibSummandOrderTarget := by
  simp only [PascalIdentityTarget, MathlibSummandOrderTarget, Nat.add_comm]

/-- Checked reindexing between the predecessor and restricted successor
forms; it does not transport to the unrestricted all-natural recurrence. -/
theorem pascalIdentityTarget_iff_restrictedSuccessorTarget :
    PascalIdentityTarget <-> RestrictedSuccessorTarget := by
  constructor
  · intro h r k hrk
    have hk : 1 <= k + 1 := Nat.le_add_left 1 k
    simpa using h (r + 1) (k + 1) (Nat.add_le_add_right hrk 1) hk
  · intro h m n hnm hn
    have hm : 1 <= m := hn.trans hnm
    have hn_cancel : n - 1 + 1 = n := Nat.sub_add_cancel hn
    have hm_cancel : m - 1 + 1 = m := Nat.sub_add_cancel hm
    simpa only [hn_cancel, hm_cancel] using
      h (m - 1) (n - 1) (Nat.sub_le_sub_right hnm 1)

/-! Structural mutations used by the statement-identity checker. -/

/-- Removed-hypothesis mutation: the source's positive-column premise is
deleted, admitting column zero where the displayed recurrence is false. -/
def mutationRemovedPositiveColumnHypothesis : Prop :=
  forall (m n : Nat), n <= m ->
    Nat.choose m n =
      Nat.choose (m - 1) n + Nat.choose (m - 1) (n - 1)

/-- Changed-domain mutation: the row and column range only over the finite
domain below ten rather than over every natural number. -/
def mutationChangedDomainToFinTen : Prop :=
  forall (m n : Fin 10), (n : Nat) <= (m : Nat) -> 1 <= (n : Nat) ->
    Nat.choose (m : Nat) (n : Nat) =
      Nat.choose ((m : Nat) - 1) (n : Nat) +
        Nat.choose ((m : Nat) - 1) ((n : Nat) - 1)

/-- Changed-binder-scope mutation: the column is existential instead of
universally quantified. -/
def mutationChangedColumnBinderScope : Prop :=
  forall (m : Nat), exists n : Nat,
    n <= m /\ 1 <= n /\
      Nat.choose m n =
        Nat.choose (m - 1) n + Nat.choose (m - 1) (n - 1)

/-- Boundary mutation: the diagonal `n = m`, included by DLMF, is excluded. -/
def mutationExcludesDiagonal : Prop :=
  forall (m n : Nat), n < m -> 1 <= n ->
    Nat.choose m n =
      Nat.choose (m - 1) n + Nat.choose (m - 1) (n - 1)

#check_failure
  (rfl : PascalIdentityTarget = mutationRemovedPositiveColumnHypothesis)
#check_failure
  (rfl : PascalIdentityTarget = mutationChangedDomainToFinTen)
#check_failure
  (rfl : PascalIdentityTarget = mutationChangedColumnBinderScope)
#check_failure
  (rfl : PascalIdentityTarget = mutationExcludesDiagonal)

/-- Any positive diagonal index satisfies the canonical source premises. -/
theorem pascalIdentityTarget_includes_diagonal
    (h : PascalIdentityTarget) (m : Nat) (hm : 1 <= m) :
    Nat.choose m m =
      Nat.choose (m - 1) m + Nat.choose (m - 1) (m - 1) :=
  h m m (Nat.le_refl m) hm

/-- Column zero is outside the canonical source domain. -/
theorem column_zero_is_excluded :
    Not (1 <= (0 : Nat)) := by
  simp

/-- An out-of-range column is outside the canonical source domain. -/
theorem out_of_range_is_excluded {m n : Nat} (h : m < n) :
    Not (n <= m) :=
  Nat.not_le_of_lt h

/-- The first admissible pair `(m,n) = (1,1)` satisfies the displayed
recurrence by computation. -/
theorem first_admissible_pair :
    Nat.choose 1 1 = Nat.choose (1 - 1) 1 + Nat.choose (1 - 1) (1 - 1) := by
  decide

/-- Removing positivity admits `(0,0)`, where the truncated predecessor
formula is false. -/
theorem positivity_hypothesis_is_semantic :
    Nat.choose 0 0 != Nat.choose (0 - 1) 0 + Nat.choose (0 - 1) (0 - 1) := by
  decide

/-- The changed-domain mutation omits canonical natural row ten. -/
theorem row_ten_has_no_fin_ten_representation :
    Not (Exists fun x : Fin 10 => (x : Nat) = 10) := by
  intro h
  obtain ⟨x, hx⟩ := h
  exact (Nat.ne_of_lt x.isLt) hx

/-- The existential-binder mutation is already false at row zero: it asks
for a positive column below zero instead of quantifying conditionally. -/
theorem existential_column_scope_fails_at_zero :
    Not (Exists fun n : Nat => n <= 0 /\ 1 <= n /\
      Nat.choose 0 n = Nat.choose (0 - 1) n + Nat.choose (0 - 1) (n - 1)) := by
  simp

/-- A diagonal index can never satisfy the strict premise introduced by the
boundary mutation. -/
theorem strict_boundary_excludes_diagonal (m : Nat) :
    Not (m < m) :=
  Nat.lt_irrefl m

/-- The zero-extended successor recurrence covers an out-of-range pair that
the source premise excludes, demonstrating why it is not the root target. -/
theorem unrestricted_successor_is_broader :
    Nat.choose 1 2 = Nat.choose 0 2 + Nat.choose 0 1 /\
      Not ((2 : Nat) <= 1) := by
  decide

#print axioms pascalIdentityTarget_iff_dlmfConjunctionTarget
#print axioms pascalIdentityTarget_iff_mathlibSummandOrderTarget
#print axioms pascalIdentityTarget_iff_restrictedSuccessorTarget
#print axioms pascalIdentityTarget_includes_diagonal
#print axioms column_zero_is_excluded
#print axioms out_of_range_is_excluded
#print axioms first_admissible_pair
#print axioms positivity_hypothesis_is_semantic
#print axioms row_ten_has_no_fin_ten_representation
#print axioms existential_column_scope_fails_at_zero
#print axioms strict_boundary_excludes_diagonal
#print axioms unrestricted_successor_is_broader

end Stage1Instances.THM_M_0912

set_option pp.explicit true in
set_option pp.universes true in
#print Stage1Instances.THM_M_0912.PascalIdentityTarget
