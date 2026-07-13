import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Combinatorics.Additive.AP.Three.Defs

/-!
# THM-M-0957 canonical Lean statement

This module freezes Behrend's historical eventual lower bound on the largest subset of
`{0, ..., N}` with no three distinct terms in arithmetic progression. It contains statement
transports only, not a proof of the bound.
-/

set_option autoImplicit false

namespace Stage1Instances.THM_M_0957

/-- The source's literal nontrivial-progression exclusion over natural numbers.

Here `a` and `c` are the endpoints and `b` is the middle term. The pairwise inequalities encode
the source's phrase "three distinct terms".
-/
def SourceThreeAPFree (s : Set Nat) : Prop :=
  forall a, a ∈ s -> forall b, b ∈ s -> forall c, c ∈ s ->
    a ≠ b -> a ≠ c -> b ≠ c -> a + c ≠ b + b

/-- The historical Behrend claim, with `rothNumberNat (N + 1)` representing the inclusive
interval `{0, ..., N}`.

`Real.log` fixes the natural-log convention, and real exponentiation is `Real.rpow` through the
`HPow Real Real Real` instance. "Sufficiently large" is encoded by an epsilon-dependent natural
threshold and a non-strict threshold comparison.
-/
def BehrendConstructionTarget : Prop :=
  forall epsilon : Real, 0 < epsilon ->
    exists N0 : Nat, forall N : Nat, N0 <= N ->
      (N : Real) ^
          (1 - (2 * Real.sqrt (2 * Real.log 2) + epsilon) /
            Real.sqrt (Real.log (N : Real))) <
        (rothNumberNat (N + 1) : Real)

/-- Direct finite-set form of the same historical claim. This spells out the inclusive interval,
literal source predicate, and set-cardinality lower bound instead of using the Roth extremum.
-/
def BehrendFiniteSetTarget : Prop :=
  forall epsilon : Real, 0 < epsilon ->
    exists N0 : Nat, forall N : Nat, N0 <= N ->
      exists s : Finset Nat,
        (forall x, x ∈ s -> x <= N) ∧
        SourceThreeAPFree (s : Set Nat) ∧
        (N : Real) ^
            (1 - (2 * Real.sqrt (2 * Real.log 2) + epsilon) /
              Real.sqrt (Real.log (N : Real))) <
          (s.card : Real)

/-- Over `Nat`, the source's exclusion of pairwise-distinct triples is exactly mathlib's
`ThreeAPFree` predicate. Cancellation forces a progression with any two equal terms to be
constant.
-/
theorem sourceThreeAPFree_iff_threeAPFree (s : Set Nat) :
    SourceThreeAPFree s <-> ThreeAPFree s := by
  rw [threeAPFree_iff_eq_right]
  constructor
  · intro hs a ha b hb c hc habc
    by_contra hac
    have hab : a ≠ b := by
      intro hab
      subst b
      apply hac
      exact (Nat.add_left_cancel habc).symm
    have hbc : b ≠ c := by
      intro hbc
      subst c
      exact hab (Nat.add_right_cancel habc)
    exact hs a ha b hb c hc hab hac hbc habc
  · intro hs a ha b hb c hc _hab hac _hbc habc
    exact hac (hs ha hb hc habc)

/-- Checked source-to-formal transport: the Roth-extremum statement is equivalent to the direct
existence of a source-predicate set in the inclusive interval.
-/
theorem behrendConstructionTarget_iff_finiteSet :
    BehrendConstructionTarget <-> BehrendFiniteSetTarget := by
  constructor
  · intro h epsilon hepsilon
    obtain ⟨N0, hN0⟩ := h epsilon hepsilon
    refine ⟨N0, ?_⟩
    intro N hN
    obtain ⟨s, hsrange, hscard, hsfree⟩ := rothNumberNat_spec (N + 1)
    refine ⟨s, ?_, (sourceThreeAPFree_iff_threeAPFree s).2 hsfree, ?_⟩
    · intro x hx
      exact Nat.lt_succ_iff.mp (Finset.mem_range.mp (hsrange hx))
    · simpa [hscard] using hN0 N hN
  · intro h epsilon hepsilon
    obtain ⟨N0, hN0⟩ := h epsilon hepsilon
    refine ⟨N0, ?_⟩
    intro N hN
    obtain ⟨s, hsN, hsfree, hsbound⟩ := hN0 N hN
    have hcard : s.card <= rothNumberNat (N + 1) :=
      ((sourceThreeAPFree_iff_threeAPFree s).1 hsfree).le_rothNumberNat s
        (fun x hx => Nat.lt_succ_iff.mpr (hsN x hx)) rfl
    exact hsbound.trans_le (Nat.cast_le.mpr hcard)

/-! Structural mutations used only by the statement-identity checker. -/

/-- Removed-hypothesis mutation: epsilon need not be positive. -/
def mutationRemovedPositiveEpsilon : Prop :=
  forall epsilon : Real,
    exists N0 : Nat, forall N : Nat, N0 <= N ->
      (N : Real) ^
          (1 - (2 * Real.sqrt (2 * Real.log 2) + epsilon) /
            Real.sqrt (Real.log (N : Real))) <
        (rothNumberNat (N + 1) : Real)

/-- Changed-domain mutation: epsilon is rational rather than real. -/
def mutationRationalEpsilon : Prop :=
  forall epsilon : Rat, 0 < epsilon ->
    exists N0 : Nat, forall N : Nat, N0 <= N ->
      (N : Real) ^
          (1 - (2 * Real.sqrt (2 * Real.log 2) + (epsilon : Real)) /
            Real.sqrt (Real.log (N : Real))) <
        (rothNumberNat (N + 1) : Real)

/-- Changed-scope mutation: one threshold must work uniformly for every positive epsilon. -/
def mutationUniformThreshold : Prop :=
  exists N0 : Nat, forall epsilon : Real, 0 < epsilon -> forall N : Nat, N0 <= N ->
    (N : Real) ^
        (1 - (2 * Real.sqrt (2 * Real.log 2) + epsilon) /
          Real.sqrt (Real.log (N : Real))) <
      (rothNumberNat (N + 1) : Real)

/-- Boundary mutation: the extremal set lies in the exclusive interval `{0, ..., N - 1}`. -/
def mutationExclusiveInterval : Prop :=
  forall epsilon : Real, 0 < epsilon ->
    exists N0 : Nat, forall N : Nat, N0 <= N ->
      (N : Real) ^
          (1 - (2 * Real.sqrt (2 * Real.log 2) + epsilon) /
            Real.sqrt (Real.log (N : Real))) <
        (rothNumberNat N : Real)

#check_failure (rfl : BehrendConstructionTarget = mutationRemovedPositiveEpsilon)
#check_failure (rfl : BehrendConstructionTarget = mutationRationalEpsilon)
#check_failure (rfl : BehrendConstructionTarget = mutationUniformThreshold)
#check_failure (rfl : BehrendConstructionTarget = mutationExclusiveInterval)

#print axioms sourceThreeAPFree_iff_threeAPFree
#print axioms behrendConstructionTarget_iff_finiteSet

end Stage1Instances.THM_M_0957

set_option pp.explicit true in
set_option pp.universes true in
#print Stage1Instances.THM_M_0957.BehrendConstructionTarget
