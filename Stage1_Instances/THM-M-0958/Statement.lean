import Mathlib.Combinatorics.Additive.AP.Three.Defs
import Mathlib.Analysis.SpecialFunctions.Log.Base

/-!
# THM-M-0958: Elkin's improved progression-free-set lower bound

This module freezes the asymptotic construction stated in Elkin's paper. The
canonical target uses the source interval `{1, ..., n}` and an explicit set
witness. Checked transports connect it to the corresponding extremal-number
form and to mathlib's zero-based `rothNumberNat` encoding. This file contains
no proof of the Elkin lower bound.
-/

noncomputable section

open Finset

namespace Stage1Instances.THM_M_0958

/-- The quantitative scale in Elkin's improvement, with both logarithms in
base two as stipulated by the source. -/
def elkinScale (n : Nat) : Real :=
  ((n : Real) /
      (2 : Real) ^ (2 * Real.sqrt 2 * Real.sqrt (Real.logb 2 (n : Real)))) *
    (Real.logb 2 (n : Real)) ^ (1 / 4 : Real)

/-- The paper's distinct-triple formulation of progression-freeness, normalized
so `b` occupies the middle of the putative progression. The universal binders
range over every ordering of the three source elements. -/
def SourceProgressionFree (s : Set Nat) : Prop :=
  forall a, a ∈ s -> forall b, b ∈ s -> forall d, d ∈ s ->
    a ≠ b -> b ≠ d -> a ≠ d -> a + d ≠ b + b

/-- On natural numbers, the source's distinct-triple predicate agrees with
mathlib's `ThreeAPFree`: a nonconstant solution of `a + d = b + b` has three
distinct entries. -/
theorem sourceProgressionFree_iff_threeAPFree (s : Set Nat) :
    SourceProgressionFree s <-> ThreeAPFree s := by
  constructor
  · intro hs a ha b hb d hd habd
    by_contra hab
    have hbd : b ≠ d := by
      intro h
      apply hab
      omega
    have had : a ≠ d := by
      intro h
      apply hab
      omega
    exact hs a ha b hb d hd hab hbd had habd
  · intro hs a ha b hb d hd hab hbd had habd
    exact hab (hs ha hb hd habd)

/-- The exact source extremal-function target. There are positive universal
constants `c` and `N` such that the largest progression-free subset of
`{1, ..., n}` has cardinality at least `c * elkinScale n` for every `n >= N`.

The source's `Omega` convention is expanded into the ordered constant,
threshold, and index binders. The lower bound is compared in `Real`, while the
set and its cardinality remain finite and natural-valued.
-/
def ElkinConstructionTarget : Prop :=
  exists c : Real, 0 < c ∧ exists N : Nat, 0 < N ∧ forall n : Nat, N ≤ n ->
    c * elkinScale n ≤ (addRothNumber (Ico 1 (n + 1)) : Real)

/-- Construction-witness expansion of the source extremal target. -/
def WitnessConstructionTarget : Prop :=
  exists c : Real, 0 < c ∧ exists N : Nat, 0 < N ∧ forall n : Nat, N ≤ n ->
    exists s : Finset Nat,
      s ⊆ Ico 1 (n + 1) ∧
        SourceProgressionFree (s : Set Nat) ∧
          c * elkinScale n ≤ (s.card : Real)

/-- Mathlib's zero-based extremal-number form. -/
def RothNumberTarget : Prop :=
  exists c : Real, 0 < c ∧ exists N : Nat, 0 < N ∧ forall n : Nat, N ≤ n ->
    c * elkinScale n ≤ (rothNumberNat n : Real)

/-- Translation by one identifies the source interval extremum with
mathlib's Roth number. -/
theorem oneBasedRothNumber_eq_rothNumberNat (n : Nat) :
    addRothNumber (Ico 1 (n + 1)) = rothNumberNat n := by
  simpa using addRothNumber_Ico 1 (n + 1)

/-- Checked transport between the source extremal and explicit construction
forms. -/
theorem elkinConstructionTarget_iff_witnessConstructionTarget :
    ElkinConstructionTarget <-> WitnessConstructionTarget := by
  constructor
  · rintro ⟨c, hc, N, hN, h⟩
    refine ⟨c, hc, N, hN, fun n hn => ?_⟩
    obtain ⟨s, hs, hcard, hfree⟩ := addRothNumber_spec (Ico 1 (n + 1))
    refine ⟨s, hs, (sourceProgressionFree_iff_threeAPFree s).mpr hfree, ?_⟩
    simpa [hcard] using h n hn
  · rintro ⟨c, hc, N, hN, h⟩
    refine ⟨c, hc, N, hN, fun n hn => ?_⟩
    obtain ⟨s, hs, hfree, hcard⟩ := h n hn
    have hsLe : s.card ≤ addRothNumber (Ico 1 (n + 1)) :=
      ((sourceProgressionFree_iff_threeAPFree s).mp hfree).le_addRothNumber hs
    exact hcard.trans (by exact_mod_cast hsLe)

/-- Checked one-based to zero-based interval transport for the exact
quantitative target. -/
theorem oneBasedExtremalTarget_iff_rothNumberTarget :
    ElkinConstructionTarget <-> RothNumberTarget := by
  simp only [ElkinConstructionTarget, RothNumberTarget,
    oneBasedRothNumber_eq_rothNumberNat]

/-- Checked composite transport from the source construction to mathlib's
extremal function. -/
theorem elkinConstructionTarget_iff_rothNumberTarget :
    ElkinConstructionTarget <-> RothNumberTarget :=
  oneBasedExtremalTarget_iff_rothNumberTarget

/-! Structural statement mutations. Each elaborates, but changes the frozen
proposition and receives no statement-identity credit. -/

/-- Removed-hypothesis mutation: the universal lower-bound constant need not
be positive, making zero an admissible choice. -/
def mutationRemovedPositiveConstant : Prop :=
  exists c : Real, exists N : Nat, 0 < N ∧ forall n : Nat, N ≤ n ->
    c * elkinScale n ≤ (addRothNumber (Ico 1 (n + 1)) : Real)

/-- Changed-domain mutation: the asymptotic index and threshold are integers,
then projected back to naturals. -/
def mutationIntegerIndexDomain : Prop :=
  exists c : Real, 0 < c ∧ exists N : Int, 0 < N ∧ forall n : Int, N ≤ n ->
    c * elkinScale n.toNat ≤
      (addRothNumber (Ico 1 (n.toNat + 1)) : Real)

/-- Changed-scope mutation: the constant may depend on `n` instead of being
uniform over the asymptotic tail. -/
def mutationPerIndexConstant : Prop :=
  exists N : Nat, 0 < N ∧ forall n : Nat, N ≤ n ->
    exists c : Real, 0 < c ∧
      c * elkinScale n ≤ (addRothNumber (Ico 1 (n + 1)) : Real)

/-- Boundary mutation: the source interval loses its inclusive upper endpoint,
replacing `{1, ..., n}` by `{1, ..., n - 1}`. -/
def mutationShiftsIntervalEndpoint : Prop :=
  exists c : Real, 0 < c ∧ exists N : Nat, 0 < N ∧ forall n : Nat, N ≤ n ->
    c * elkinScale n ≤ (addRothNumber (Ico 1 n) : Real)

#check_failure
  (rfl : ElkinConstructionTarget = mutationRemovedPositiveConstant)
#check_failure
  (rfl : ElkinConstructionTarget = mutationIntegerIndexDomain)
#check_failure
  (rfl : ElkinConstructionTarget = mutationPerIndexConstant)
#check_failure
  (rfl : ElkinConstructionTarget = mutationShiftsIntervalEndpoint)

/-- The totalized real expression has the expected zero value at `n = 0`. -/
theorem elkinScale_zero : elkinScale 0 = 0 := by
  norm_num [elkinScale]

/-- The totalized real expression has the expected zero value at `n = 1`. -/
theorem elkinScale_one : elkinScale 1 = 0 := by
  norm_num [elkinScale, Real.logb]

/-- The one-based interval is empty at the zero boundary. -/
theorem oneBasedInterval_zero : Ico 1 (0 + 1) = (∅ : Finset Nat) := by
  decide

/-- The one-based interval is the expected singleton at `n = 1`. -/
theorem oneBasedInterval_one : Ico 1 (1 + 1) = ({1} : Finset Nat) := by
  decide

#print axioms sourceProgressionFree_iff_threeAPFree
#print axioms oneBasedRothNumber_eq_rothNumberNat
#print axioms elkinConstructionTarget_iff_witnessConstructionTarget
#print axioms oneBasedExtremalTarget_iff_rothNumberTarget
#print axioms elkinConstructionTarget_iff_rothNumberTarget
#print axioms elkinScale_zero
#print axioms elkinScale_one
#print axioms oneBasedInterval_zero
#print axioms oneBasedInterval_one

end Stage1Instances.THM_M_0958

set_option pp.explicit true in
set_option pp.universes true in
#print Stage1Instances.THM_M_0958.ElkinConstructionTarget
